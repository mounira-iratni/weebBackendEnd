"""Serializers for blog articles."""

from rest_framework import serializers
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    """Simplified serializer for article listings."""

    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "excerpt", "author_name", "created_at", "published"]
        read_only_fields = ["id", "created_at", "published"]

    def get_author_name(self, obj):
        """Return the full name of the article author."""
        return f"{obj.author.first_name} {obj.author.last_name}".strip()


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Full article serializer with all fields."""

    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "content", "excerpt", "author_name", "created_at", "updated_at", "published"]
        read_only_fields = ["id", "created_at", "updated_at", "published"]

    def get_author_name(self, obj):
        """Return the full name of the article author."""
        return f"{obj.author.first_name} {obj.author.last_name}".strip()


class ArticleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating articles."""

    class Meta:
        model = Article
        fields = ["title", "slug", "content", "excerpt"]

    def create(self, validated_data):
        """Create article with current user as author."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)
