"""Database models for blog articles."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Article(models.Model):
    """Blog article model with author and publication tracking."""

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["published"]),
        ]

    def __str__(self):
        """Return the article title."""
        return self.title
