"""Admin registrations for blog models."""

from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for Article model."""

    list_display = ("title", "author", "created_at", "published")
    list_filter = ("published", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "author")}),
        ("Content", {"fields": ("excerpt", "content")}),
        ("Publishing", {"fields": ("published",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def save_model(self, request, obj, form, change):
        """Set author to current user if not set."""
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
