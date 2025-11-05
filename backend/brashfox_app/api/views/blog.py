"""
Blog-related ViewSets: BlogPost, PostCategory
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from brashfox_app.models import BlogPost, PostCategory
from brashfox_app.api.serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    PostCategorySerializer,
    PostCommentsSerializer,
)
from brashfox_app.api.permissions import (
    IsAuthorOrReadOnly,
    IsAdminOrReadOnly,
)
from brashfox_app.api.services import BlogPostService


class BlogPostViewSet(ModelViewSet):
    """
    API endpoint for blog posts.
    - Read: Anyone
    - Create: Authenticated users
    - Update/Delete: Author or Admin only
    Uses different serializers for list and detail views.
    Supports lookup by slug or pk.
    Automatically sets author to current user on create.
    """
    queryset = BlogPost.objects.select_related('author').all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = ['author']
    search_fields = ['title', 'post']
    ordering_fields = ['created', 'edited', 'title']
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return BlogPostDetailSerializer
        return BlogPostListSerializer
    
    def perform_create(self, serializer):
        """Automatically set author to current user"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        """Get all comments for a post using service"""
        post = self.get_object()
        comments = BlogPostService.get_post_comments(post)
        serializer = PostCommentsSerializer(comments, many=True)
        return Response(serializer.data)


class PostCategoryViewSet(ModelViewSet):
    """
    API endpoint for post categories.
    - Read: Anyone
    - Write: Admins only
    """
    queryset = PostCategory.objects.prefetch_related('blog_post').all()
    serializer_class = PostCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['category']
    ordering_fields = ['category']
