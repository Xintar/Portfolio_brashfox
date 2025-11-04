from django.contrib.auth.models import Group, User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

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
    GroupSerializer,
    FotoCategorySerializer,
    FotoDescriptionSerializer,
    FotoTagsSerializer,
    BlogPostSerializer,
    PostCategorySerializer,
    PostCommentsSerializer,
    MessageSerializer,
)


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class GroupViewSet(ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class FotoCategoryViewSet(ModelViewSet):
    queryset = FotoCategory.objects.all()
    serializer_class = FotoCategorySerializer
    
class FotoDescriptionViewSet(ModelViewSet):
    queryset = FotoDescription.objects.all()
    serializer_class = FotoDescriptionSerializer
    
class FotoTagsViewSet(ModelViewSet):
    queryset = FotoTags.objects.all()
    serializer_class = FotoTagsSerializer

class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    
class PostCategoryViewSet(ModelViewSet):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer
    
class PostCommentsViewSet(ModelViewSet):
    queryset = PostComments.objects.all()
    serializer_class = PostCommentsSerializer
    
class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
