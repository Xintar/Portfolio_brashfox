from rest_framework.viewsets import ModelViewSet
from brashfox_app.models import BlogPost
from brashfox_app.api.serializers import BlogPostSerializer


class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    