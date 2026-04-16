from django.contrib import admin
from .models import Part, PCBuild, BuildItem


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    """Admin configuration for Part model with search, filters, and display options."""
    list_display = ['name', 'manufacturer', 'part_type', 'price', 'wattage', 'status', 'created_at']
    list_filter = ['part_type', 'status', 'created_at', 'manufacturer']
    search_fields = ['name', 'manufacturer', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'manufacturer', 'part_type')
        }),
        ('Specifications', {
            'fields': ('wattage', 'price', 'status'),
            'classes': ('collapse',),
        }),
        ('Details', {
            'fields': ('description', 'image'),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


class BuildItemInline(admin.TabularInline):
    """Inline admin for BuildItem to edit parts directly in Build admin."""
    model = BuildItem
    extra = 1
    fields = ['part', 'quantity']
    raw_id_fields = ['part']


@admin.register(PCBuild)
class PCBuildAdmin(admin.ModelAdmin):
    """Admin configuration for PCBuild model with inline editing."""
    list_display = ['name', 'creator', 'total_budget', 'get_total_cost_display', 'is_public', 'created_at']
    list_filter = ['creator', 'is_public', 'created_at']
    search_fields = ['name', 'creator__username', 'slug']
    readonly_fields = ['creator', 'created_at', 'updated_at', 'slug', 'get_total_cost', 'get_remaining_budget', 'get_total_wattage', 'get_recommended_psu']
    inlines = [BuildItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'creator')
        }),
        ('Budget & Details', {
            'fields': ('total_budget', 'notes', 'description', 'image')
        }),
        ('Settings', {
            'fields': ('is_public',)
        }),
        ('Calculated Values', {
            'fields': ('get_total_cost', 'get_remaining_budget', 'get_total_wattage', 'get_recommended_psu'),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def get_total_cost_display(self, obj):
        """Display total cost in list view."""
        return f"${obj.get_total_cost():.2f}"
    get_total_cost_display.short_description = "Total Cost"
    
    def save_model(self, request, obj, form, change):
        """Set creator to current user when creating new build."""
        if not change:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


@admin.register(BuildItem)
class BuildItemAdmin(admin.ModelAdmin):
    """Admin configuration for BuildItem model."""
    list_display = ['pc_build', 'part', 'quantity', 'get_total_price_display', 'added_at']
    list_filter = ['added_at', 'pc_build', 'part__part_type']
    search_fields = ['pc_build__name', 'part__name']
    ordering = ['-added_at']
    readonly_fields = ['added_at']
    
    def get_total_price_display(self, obj):
        """Display total price for this line item."""
        return f"${obj.get_total_price():.2f}"
    get_total_price_display.short_description = "Line Total"
