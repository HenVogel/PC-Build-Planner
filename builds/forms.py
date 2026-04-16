from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Part, PCBuild, BuildItem


class PartForm(forms.ModelForm):
    """Form for creating and editing Part objects."""
    class Meta:
        model = Part
        fields = ['name', 'manufacturer', 'part_type', 'wattage', 'price', 'status', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Part name'}),
            'manufacturer': forms.TextInput(attrs={'placeholder': 'Brand/Manufacturer'}),
            'part_type': forms.Select(),
            'wattage': forms.NumberInput(attrs={'placeholder': 'Wattage (optional)'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Price'}),
            'status': forms.Select(),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Detailed specifications...'}),
            'image': forms.FileInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Part Information',
                Row(
                    Column('name', css_class='col-md-6'),
                    Column('manufacturer', css_class='col-md-6'),
                ),
                Row(
                    Column('part_type', css_class='col-md-4'),
                    Column('price', css_class='col-md-4'),
                    Column('wattage', css_class='col-md-4'),
                ),
                'status',
                'description',
                'image',
            ),
            Submit('submit', 'Save Part', css_class='btn btn-primary')
        )


class PCBuildForm(forms.ModelForm):
    """Form for creating and editing PCBuild objects."""
    class Meta:
        model = PCBuild
        fields = ['name', 'total_budget', 'notes', 'description', 'image', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Build name'}),
            'total_budget': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Total budget'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quick notes...'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Detailed build guide (Markdown supported)...'}),
            'image': forms.FileInput(),
            'is_public': forms.CheckboxInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Build Details',
                Row(
                    Column('name', css_class='col-md-8'),
                    Column('total_budget', css_class='col-md-4'),
                ),
                'notes',
                'description',
                'image',
                'is_public',
            ),
            Submit('submit', 'Save Build', css_class='btn btn-primary')
        )


class BuildItemForm(forms.ModelForm):
    """Form for adding parts to a build."""
    part = forms.ModelChoiceField(
        queryset=Part.objects.all(),
        label='Select Part',
        widget=forms.Select()
    )
    
    class Meta:
        model = BuildItem
        fields = ['part', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': '1', 'value': '1'}),
        }
    
    def clean(self):
        """Validate that single-only parts don't exceed quantity 1."""
        cleaned_data = super().clean()
        part = cleaned_data.get('part')
        quantity = cleaned_data.get('quantity')
        
        if part and quantity and not part.allows_multiple() and quantity > 1:
            raise forms.ValidationError(
                f'{part.name} can only be added once per build. Please set quantity to 1.'
            )
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('part', css_class='col-md-8'),
                Column('quantity', css_class='col-md-4'),
            ),
            Submit('submit', 'Add Part', css_class='btn btn-success')
        )


class BuildItemUpdateForm(forms.ModelForm):
    """Form for updating BuildItem (swap parts, change quantity)."""
    part = forms.ModelChoiceField(
        queryset=Part.objects.all(),
        label='Select Part',
        widget=forms.Select()
    )
    
    class Meta:
        model = BuildItem
        fields = ['part', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': '1'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('part', css_class='col-md-8'),
                Column('quantity', css_class='col-md-4'),
            ),
            Submit('submit', 'Update Part', css_class='btn btn-primary')
        )


class UserLoginForm(AuthenticationForm):
    """Custom form for user login."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login', css_class='btn btn-primary w-100 mt-3')
        )


class UserSignUpForm(UserCreationForm):
    """Custom form for user registration."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control',
                'autofocus': True,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        })
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Create Your Account',
                'username',
                'email',
                'password1',
                'password2',
            ),
            Submit('submit', 'Sign Up', css_class='btn btn-success w-100 mt-3')
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


class UserEmailForm(forms.Form):
    """Form for updating the user's email address."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control',
        })
    )


class UserPasswordForm(PasswordChangeForm):
    """Form for updating the user's password."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
