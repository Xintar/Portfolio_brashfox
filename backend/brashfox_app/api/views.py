from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from brashfox_app.models import BlogPost
from brashfox_app.api.serializers import (
    BlogPostSerializer,
    UserSerializer,
    GroupSerializer,
)


class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
