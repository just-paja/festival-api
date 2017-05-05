"""Site administration module."""
from django.contrib import admin

DEFAULT_READONLY = ['created_at', 'updated_at']


class BaseAdminModel(admin.ModelAdmin):
    """Base admin for models."""

    def get_readonly_fields(self, request, obj=None):
        """Define default readonly fields."""
        return DEFAULT_READONLY + list(self.readonly_fields)


class BaseInlineAdminModel(admin.TabularInline):
    """Base admin for Inline models."""

    def get_readonly_fields(self, request, obj=None):
        """Define default readonly fields."""
        return DEFAULT_READONLY + list(self.readonly_fields)


class BaseTextAdminModel(BaseAdminModel):
    """Base admin for Text models."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'updated_at')


class BaseTagAdmin(BaseAdminModel):
    """Admin model for tag-like models."""

    prepopulated_fields = {'slug': ('name',)}


class FoodAdminMixin():
    list_display = (
        'name',
        'meal',
        'capacity',
        'created_at',
        'visibility',
    )