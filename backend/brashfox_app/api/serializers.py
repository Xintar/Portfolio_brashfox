from django.contrib.auth.models import Group, User
from rest_framework.serializers import (
    ModelSerializer, 
    HyperlinkedModelSerializer,
)
from brashfox_app.models import BlogPost


class BlogPostSerializer(ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
      
class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']  