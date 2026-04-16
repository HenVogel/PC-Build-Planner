from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.urls import reverse


class Part(models.Model):
    """Model representing a PC component part (Component)."""
    PART_TYPES = [
        ('CPU', 'CPU'),
        ('GPU', 'GPU'),
        ('RAM', 'RAM'),
        ('SSD', 'SSD'),
        ('HDD', 'HDD'),
        ('PSU', 'Power Supply'),
        ('CASE', 'Case'),
        ('MOTHERBOARD', 'Motherboard'),
        ('COOLER', 'CPU Cooler'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('IN_STOCK', 'In Stock'),
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('DISCONTINUED', 'Discontinued'),
    ]
    
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255, blank=True, help_text="Brand/Manufacturer name")
    part_type = models.CharField(max_length=20, choices=PART_TYPES)
    wattage = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], help_text="Power consumption in watts")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_STOCK')
    description = models.TextField(blank=True, help_text="Detailed specifications and description")
    image = models.ImageField(upload_to='parts/', null=True, blank=True, help_text="Component image")
    favorited_by = models.ManyToManyField(User, related_name='favorite_parts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_part_type_display()})"
    
    def get_status_badge_class(self):
        """Return Bootstrap badge class for status."""
        status_map = {
            'IN_STOCK': 'success',
            'OUT_OF_STOCK': 'warning',
            'DISCONTINUED': 'danger',
        }
        return status_map.get(self.status, 'secondary')
    
    def allows_multiple(self):
        """Check if this part type allows multiple units in a build."""
        # Parts that can only have 1 unit
        single_only = ['CPU', 'MOTHERBOARD', 'PSU', 'CASE']
        return self.part_type not in single_only
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Parts'


class PCBuild(models.Model):
    """Model representing a PC build configuration."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, help_text="URL-friendly version of the build name")
    total_budget = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Total budget for the build"
    )
    notes = models.TextField(blank=True, help_text="Additional notes about the build")
    description = models.TextField(blank=True, help_text="Detailed build guide (supports Markdown)")
    image = models.ImageField(upload_to='builds/', null=True, blank=True, help_text="Build showcase image")
    is_public = models.BooleanField(default=False, help_text="Make this build visible to other users")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pc_builds')
    favorited_by = models.ManyToManyField(User, related_name='favorite_builds', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (${self.total_budget})"
    
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Return the canonical URL for the build."""
        return reverse('builds:build_detail_slug', kwargs={'slug': self.slug})
    
    def get_total_cost(self):
        """Calculate total cost of all parts in this build."""
        items = self.builditem_set.all()
        return sum(item.part.price * item.quantity for item in items)
    
    def get_remaining_budget(self):
        """Calculate remaining budget."""
        return self.total_budget - self.get_total_cost()
    
    def get_total_wattage(self):
        """Calculate total wattage required by PSU."""
        items = self.builditem_set.all()
        return sum((item.part.wattage or 0) * item.quantity for item in items)
    
    def get_recommended_psu(self):
        """Recommend PSU wattage based on components (add 20% headroom)."""
        total_wattage = self.get_total_wattage()
        if total_wattage == 0:
            return 0
        recommended = int(total_wattage * 1.2)
        # Round up to nearest 50W for common PSU sizes
        return ((recommended + 49) // 50) * 50
    
    def get_budget_percentage(self):
        """Get percentage of budget used."""
        if self.total_budget == 0:
            return 0
        return min(100, int((self.get_total_cost() / self.total_budget) * 100))
    
    class Meta:
        ordering = ['-created_at']


class BuildItem(models.Model):
    """Model linking a Part to a PCBuild (many-to-many with metadata)."""
    pc_build = models.ForeignKey(PCBuild, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.pc_build.name} - {self.part.name} (x{self.quantity})"
    
    def get_total_price(self):
        """Get total price for this line item."""
        return self.part.price * self.quantity
    
    class Meta:
        unique_together = ('pc_build', 'part')
        ordering = ['-added_at']
        verbose_name_plural = 'Build Items'
