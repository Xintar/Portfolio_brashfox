"""
Comment-related ViewSets: PostComments
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from brashfox_app.models import PostComments
from brashfox_app.api.serializers import PostCommentsSerializer
from brashfox_app.api.permissions import IsAuthorOrReadOnly


class PostCommentsViewSet(ModelViewSet):
    """
    API endpoint for post comments.
    - Read: Anyone
    - Create: Authenticated users
    - Update/Delete: Author or Admin only
    Automatically sets author to current user on create.
    """
    queryset = PostComments.objects.select_related('blog_post', 'blog_post__author').all()
    serializer_class = PostCommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_fields = ['blog_post', 'author']
    search_fields = ['comment']
    ordering_fields = ['created']
    
    def perform_create(self, serializer):
        """Automatically set author to current user"""
        serializer.save(author=self.request.user)
