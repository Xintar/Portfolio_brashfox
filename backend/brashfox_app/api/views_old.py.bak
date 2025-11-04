from django.contrib.auth.models import Group, User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from brashfox_app.models import (
    FotoCategory,
    FotoDescription,
    FotoTags,
    BlogPost,
    PostCategory,
    PostComments,
    Message,
)
from brashfox_app.api.serializers import (
    UserSerializer,
    UserCreateSerializer,
    GroupSerializer,
    FotoCategorySerializer,
    FotoDescriptionListSerializer,
    FotoDescriptionDetailSerializer,
    FotoTagsSerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    PostCategorySerializer,
    PostCommentsSerializer,
    MessageSerializer,
)
from brashfox_app.api.permissions import (
    IsAuthorOrReadOnly,
    IsOwnerOrAdmin,
    IsAdminOrReadOnly,
)
from brashfox_app.api.throttles import (
    ContactFormThrottle,
    RegisterThrottle,
)


class UserViewSet(ModelViewSet):
    """
    API endpoint for users.
    - List/Retrieve: Authenticated users only
    - Create: Anyone (registration) - rate limited to 3/hour
    - Update/Delete: Owner or Admin only
    """
    queryset = User.objects.all().order_by('-date_joined')
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]
    
    def get_throttles(self):
        """Apply stricter rate limiting to registration"""
        if self.action == 'create':
            return [RegisterThrottle()]
        return super().get_throttles()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class GroupViewSet(ModelViewSet):
    """
    API endpoint for groups.
    Requires authentication.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class FotoCategoryViewSet(ModelViewSet):
    """
    API endpoint for photo categories.
    - Read: Anyone
    - Write: Admins only
    """
    queryset = FotoCategory.objects.all()
    serializer_class = FotoCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    

class FotoDescriptionViewSet(ModelViewSet):
    """
    API endpoint for photos.
    - Read: Anyone
    - Create: Authenticated users
    - Update/Delete: Author or Admin only
    Uses different serializers for list and detail views.
    Automatically sets author to current user on create.
    """
    queryset = FotoDescription.objects.select_related('foto_category').all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_fields = ['foto_category', 'author']
    search_fields = ['name', 'author', 'event']
    ordering_fields = ['created', 'edited', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FotoDescriptionDetailSerializer
        return FotoDescriptionListSerializer
    
    def perform_create(self, serializer):
        """Automatically set author to current user"""
        serializer.save(author=self.request.user.username)
    

class FotoTagsViewSet(ModelViewSet):
    """
    API endpoint for photo tags.
    - Read: Anyone
    - Write: Authenticated users only
    """
    queryset = FotoTags.objects.prefetch_related('foto_description').all()
    serializer_class = FotoTagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['tags']
    ordering_fields = ['tags']


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
        """Get all comments for a post"""
        post = self.get_object()
        comments = post.comments.all()
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


class PostCommentsViewSet(ModelViewSet):
    """
    API endpoint for post comments.
    - Read: Anyone
    - Create: Anyone (public comments)
    - Update/Delete: Authenticated users only
    """
    queryset = PostComments.objects.select_related('blog_post').all()
    serializer_class = PostCommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['blog_post', 'author']
    search_fields = ['comment', 'author']
    ordering_fields = ['created', 'edited']


class MessageViewSet(ModelViewSet):
    """
    API endpoint for contact messages.
    - Create: Anyone (contact form) - rate limited to 5/hour
    - Read/Update/Delete: Admins only
    """
    queryset = Message.objects.all().order_by('-created')
    serializer_class = MessageSerializer
    filterset_fields = ['email', 'topic']
    search_fields = ['name', 'email', 'topic', 'message']
    ordering_fields = ['created']
    
    def get_permissions(self):
        """Allow anyone to create (send message), but require admin for other actions"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]
    
    def get_throttles(self):
        """Apply stricter rate limiting to contact form"""
        if self.action == 'create':
            return [ContactFormThrottle()]
        return super().get_throttles()
