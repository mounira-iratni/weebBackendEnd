"""API views for blog articles."""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleCreateSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """ViewSet for article CRUD operations."""

    queryset = Article.objects.filter(published=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "create" or self.action == "update" or self.action == "partial_update":
            return ArticleCreateSerializer
        elif self.action == "retrieve":
            return ArticleDetailSerializer
        return ArticleListSerializer

    def perform_create(self, serializer):
        """Set the author to the current user when creating."""
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"])
    def my_articles(self, request):
        """Return articles authored by the current user."""
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        articles = Article.objects.filter(author=request.user)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        """Toggle published status of an article."""
        article = self.get_object()
        
        # Check ownership
        if article.author != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to edit this article."},
                status=status.HTTP_403_FORBIDDEN
            )

        article.published = not article.published
        article.save()
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)
