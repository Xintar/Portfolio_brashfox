from django.contrib.auth.models import Group, User
from rest_framework.serializers import (
    ModelSerializer, 
    HyperlinkedModelSerializer,
)

from brashfox_app.models import (
    FotoCategory,
    FotoDescription,
    FotoTags,
    BlogPost,
    PostCategory,
    PostComments,
    Message,
)

   
class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']  

class FotoCategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = FotoCategory
        fields = '__all__'

class FotoDescriptionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = FotoDescription
        fields = '__all__'

class FotoTagsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = FotoTags
        fields = '__all__'

class BlogPostSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
        
class PostCategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = PostCategory
        fields = '__all__'
        
class PostCommentsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = PostComments
        fields = '__all__'
        
class MessageSerializer(HyperlinkedModelSerializer):    
    class Meta:
        model = Message
        fields = '__all__'
