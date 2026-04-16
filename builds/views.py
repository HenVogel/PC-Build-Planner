from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
from .models import Part, PCBuild, BuildItem
from .forms import PCBuildForm, BuildItemForm, BuildItemUpdateForm, PartForm, UserLoginForm, UserSignUpForm, UserEmailForm, UserPasswordForm


# Error handlers
def handler_404(request, exception=None):
    """Handle 404 errors with custom template."""
    return render(request, 'errors/404.html', status=404)


def handler_500(request):
    """Handle 500 errors with custom template."""
    return render(request, 'errors/500.html', status=500)


class UserLoginView(LoginView):
    """Custom login view for regular users."""
    template_name = 'auth/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('builds:build_list')


class UserLogoutView(LogoutView):
    """Custom logout view."""
    next_page = reverse_lazy('home')


class UserProfileView(LoginRequiredMixin, TemplateView):
    """Display and update the current user's profile settings."""
    template_name = 'auth/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['email_form'] = kwargs.get('email_form') or UserEmailForm(initial={'email': user.email})
        context['password_form'] = kwargs.get('password_form') or UserPasswordForm(user=user)
        context['favorite_parts'] = user.favorite_parts.all().order_by('name')[:6]
        context['favorite_builds'] = user.favorite_builds.all().order_by('-updated_at')[:6]
        return context

    def post(self, request, *args, **kwargs):
        form_type = request.POST.get('form_type')

        if form_type == 'email':
            email_form = UserEmailForm(request.POST)
            password_form = UserPasswordForm(user=request.user)
            if email_form.is_valid():
                request.user.email = email_form.cleaned_data['email']
                request.user.save(update_fields=['email'])
                messages.success(request, 'Email updated successfully.')
                return redirect('builds:profile')
            return self.render_to_response(self.get_context_data(email_form=email_form, password_form=password_form))

        if form_type == 'password':
            password_form = UserPasswordForm(user=request.user, data=request.POST)
            email_form = UserEmailForm(initial={'email': request.user.email})
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated successfully.')
                return redirect('builds:profile')
            return self.render_to_response(self.get_context_data(email_form=email_form, password_form=password_form))

        return redirect('builds:profile')


class UserSignUpView(CreateView):
    """Custom signup view for new users."""
    form_class = UserSignUpForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('builds:login')
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('builds:build_list')
        return super().get(request)
    
    def form_valid(self, form):
        # New signups are always regular users; admin roles are managed in Django admin.
        form.instance.is_staff = False
        form.instance.is_superuser = False
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response


class UserIsOwnerMixin(UserPassesTestMixin):
    """Mixin to check if user is the owner of the PC build."""
    def test_func(self):
        build = self.get_object()
        return self.request.user == build.creator


class PublicBuildAccessMixin(UserPassesTestMixin):
    """Mixin to allow viewing public builds or own builds."""
    def test_func(self):
        build = self.get_object()
        return build.is_public or self.request.user == build.creator


class BuildListView(LoginRequiredMixin, ListView):
    """Display PC builds created by the logged-in user."""
    model = PCBuild
    template_name = 'builds/build_list.html'
    context_object_name = 'builds'
    paginate_by = 10
    
    def get_queryset(self):
        return PCBuild.objects.filter(creator=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_builds_count'] = PCBuild.objects.filter(creator=self.request.user).count()
        return context


class BuildCreateView(LoginRequiredMixin, CreateView):
    """Create a new PC build."""
    model = PCBuild
    form_class = PCBuildForm
    template_name = 'builds/build_form.html'
    success_url = reverse_lazy('builds:build_list')
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, f'Build "{form.instance.name}" created successfully! Start adding components.')
        return super().form_valid(form)


class BuildDetailView(PublicBuildAccessMixin, DetailView):
    """Display details of a specific PC build with all its parts and wattage info."""
    model = PCBuild
    template_name = 'builds/build_detail.html'
    context_object_name = 'build'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        build = self.object
        context['build_items'] = build.builditem_set.all()
        context['total_cost'] = build.get_total_cost()
        context['remaining_budget'] = build.get_remaining_budget()
        context['total_wattage'] = build.get_total_wattage()
        context['recommended_psu'] = build.get_recommended_psu()
        context['budget_percentage'] = build.get_budget_percentage()
        context['parts'] = Part.objects.all()
        
        # Wattage warnings
        total_watts = context['total_wattage']
        if total_watts > 0:
            context['wattage_warning'] = False
            # Check if user has PSU and if it's adequate
            psu_parts = build.builditem_set.filter(part__part_type='PSU')
            if psu_parts.exists():
                psu = psu_parts.first()
                if psu.part.wattage and psu.part.wattage < total_watts:
                    context['wattage_warning'] = True
                    context['wattage_warning_msg'] = f"Your PSU ({psu.part.wattage}W) may be insufficient for {total_watts}W of components. Consider a {context['recommended_psu']}W PSU."
            else:
                context['wattage_warning'] = True
                context['wattage_warning_msg'] = f"No PSU selected. We recommend a {context['recommended_psu']}W PSU for this build."
        
        return context
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except PCBuild.DoesNotExist:
            return handler_404(request)


class BuildDetailPkView(PublicBuildAccessMixin, DetailView):
    """Display details using primary key (legacy support)."""
    model = PCBuild
    template_name = 'builds/build_detail.html'
    context_object_name = 'build'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        build = self.object
        context['build_items'] = build.builditem_set.all()
        context['total_cost'] = build.get_total_cost()
        context['remaining_budget'] = build.get_remaining_budget()
        context['total_wattage'] = build.get_total_wattage()
        context['recommended_psu'] = build.get_recommended_psu()
        context['budget_percentage'] = build.get_budget_percentage()
        context['parts'] = Part.objects.all()
        
        # Wattage warnings
        total_watts = context['total_wattage']
        if total_watts > 0:
            context['wattage_warning'] = False
            psu_parts = build.builditem_set.filter(part__part_type='PSU')
            if psu_parts.exists():
                psu = psu_parts.first()
                if psu.part.wattage and psu.part.wattage < total_watts:
                    context['wattage_warning'] = True
                    context['wattage_warning_msg'] = f"Your PSU ({psu.part.wattage}W) may be insufficient for {total_watts}W of components. Consider a {context['recommended_psu']}W PSU."
            else:
                context['wattage_warning'] = True
                context['wattage_warning_msg'] = f"No PSU selected. We recommend a {context['recommended_psu']}W PSU for this build."
        
        return context


class BuildUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    """Update the details of a PC build."""
    model = PCBuild
    form_class = PCBuildForm
    template_name = 'builds/build_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def form_valid(self, form):
        messages.success(self.request, 'Build updated successfully!')
        return super().form_valid(form)


class BuildDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    """Delete a PC build."""
    model = PCBuild
    template_name = 'builds/build_confirm_delete.html'
    success_url = reverse_lazy('builds:build_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Build deleted successfully!')
        return super().delete(request, *args, **kwargs)


class AddPartToBuildView(LoginRequiredMixin, UserIsOwnerMixin, DetailView):
    """Add a part to a build (handles both GET and POST)."""
    model = PCBuild
    template_name = 'builds/add_part_to_build.html'
    context_object_name = 'build'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BuildItemForm()
        context['parts'] = Part.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Handle new dynamic multiple parts submission
        part_ids = request.POST.getlist('part_ids')
        
        if part_ids:
            # New format: multiple parts at once
            messages_list = []
            for part_id in part_ids:
                try:
                    part = Part.objects.get(pk=part_id)
                    
                    # For now, default to quantity 1
                    # (can be enhanced later for multi-add functionality)
                    quantity = 1
                    
                    # Validate quantity for single-only parts
                    if not part.allows_multiple():
                        # Check if part already exists
                        if BuildItem.objects.filter(pc_build=self.object, part=part).exists():
                            messages_list.append(f'{part.name} is already in this build.')
                            continue
                        quantity = 1
                    
                    # Create or update BuildItem
                    build_item, created = BuildItem.objects.get_or_create(
                        pc_build=self.object,
                        part=part,
                        defaults={'quantity': quantity}
                    )
                    
                    if not created:
                        build_item.quantity = quantity
                        build_item.save()
                        messages_list.append(f'Updated {part.name}')
                    else:
                        messages_list.append(f'Added {part.name}')
                        
                except Part.DoesNotExist:
                    pass
            
            if messages_list:
                messages.success(request, ' • '.join(messages_list))
            
            return redirect('builds:build_detail_slug', slug=self.object.slug)
        else:
            # Old format: single part
            form = BuildItemForm(request.POST)
            
            if form.is_valid():
                part = form.cleaned_data['part']
                quantity = form.cleaned_data['quantity']
                
                # Validate that single-only parts don't exceed quantity 1
                if not part.allows_multiple() and quantity > 1:
                    messages.error(request, f'{part.name} can only be added once per build.')
                    context = self.get_context_data()
                    context['form'] = form
                    return self.render_to_response(context)
                
                # Check if part already exists in build
                build_item, created = BuildItem.objects.get_or_create(
                    pc_build=self.object,
                    part=part,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    build_item.quantity = quantity
                    build_item.save()
                    messages.info(request, f'Updated quantity of {part.name} in the build.')
                else:
                    messages.success(request, f'Added {part.name} to the build!')
                
                return redirect('builds:build_detail_slug', slug=self.object.slug)
            
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class UpdateBuildItemView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    """Update a BuildItem (swap parts or change quantity)."""
    model = BuildItem
    form_class = BuildItemUpdateForm
    template_name = 'builds/builditem_form.html'
    pk_url_kwarg = 'item_pk'
    
    def test_func(self):
        item = self.get_object()
        return self.request.user == item.pc_build.creator
    
    def get_object(self, queryset=None):
        return get_object_or_404(BuildItem, pk=self.kwargs['item_pk'], pc_build__creator=self.request.user)
    
    def get_success_url(self):
        return self.object.pc_build.get_absolute_url()
    
    def form_valid(self, form):
        messages.success(self.request, 'Part updated successfully!')
        return super().form_valid(form)


class DeleteBuildItemView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    """Remove a part from a build."""
    model = BuildItem
    template_name = 'builds/builditem_confirm_delete.html'
    pk_url_kwarg = 'item_pk'
    
    def test_func(self):
        item = self.get_object()
        return self.request.user == item.pc_build.creator
    
    def get_object(self, queryset=None):
        return get_object_or_404(BuildItem, pk=self.kwargs['item_pk'], pc_build__creator=self.request.user)
    
    def get_success_url(self):
        return self.object.pc_build.get_absolute_url()
    
    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        build_slug = item.pc_build.slug
        
        # Delete the item
        item.delete()
        
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Part removed from build!'})
        
        # Handle regular requests
        messages.success(request, 'Part removed from build!')
        return redirect(self.get_success_url())


def parts_api(request):
    """API endpoint to get parts by type (for dynamic UI updates)."""
    part_type = request.GET.get('type', '')
    parts = Part.objects.filter(part_type=part_type) if part_type else Part.objects.all()
    
    return render(request, 'builds/parts_options.html', {'parts': parts})


class ToggleFavoriteBuildView(LoginRequiredMixin, DeleteView):
    """Toggle favorite status for a build."""
    model = PCBuild
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def post(self, request, *args, **kwargs):
        build = self.get_object()
        user = request.user
        
        if build.favorited_by.filter(pk=user.pk).exists():
            build.favorited_by.remove(user)
            is_favorited = False
        else:
            build.favorited_by.add(user)
            is_favorited = True
        
        return JsonResponse({'success': True, 'is_favorited': is_favorited})


class ToggleFavoritePartView(LoginRequiredMixin, DeleteView):
    """Toggle favorite status for a part."""
    model = Part
    pk_url_kwarg = 'pk'
    
    def post(self, request, *args, **kwargs):
        part = self.get_object()
        user = request.user
        
        if part.favorited_by.filter(pk=user.pk).exists():
            part.favorited_by.remove(user)
            is_favorited = False
        else:
            part.favorited_by.add(user)
            is_favorited = True
        
        return JsonResponse({'success': True, 'is_favorited': is_favorited})
