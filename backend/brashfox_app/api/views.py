from django.contrib.auth.models import Group, User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from brashfox_app.models import BlogPost
from brashfox_app.api.serializers import (
    BlogPostSerializer,
    UserSerializer,
    GroupSerializer,
)


class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

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