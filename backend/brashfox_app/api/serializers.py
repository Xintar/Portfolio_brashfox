from django.contrib.auth.models import Group, User
from rest_framework import serializers
from django.utils.text import slugify

from brashfox_app.models import (
    FotoCategory,
    FotoDescription,
    FotoTags,
    BlogPost,
    PostCategory,
    PostComments,
    Message,
)


# User Serializers
class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - used for nested representations"""
    blog_posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'blog_posts_count']
        read_only_fields = ['id']
    
    def get_blog_posts_count(self, obj):
        return obj.blog_posts.count()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users"""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        read_only_fields = ['id']


# Photo Category Serializers
class FotoCategorySerializer(serializers.ModelSerializer):
    photos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = FotoCategory
        fields = ['id', 'category', 'photos_count']
        read_only_fields = ['id']
    
    def get_photos_count(self, obj):
        return obj.photos.count()


# Photo Description Serializers
class FotoDescriptionListSerializer(serializers.ModelSerializer):
    """Serializer for listing photos - minimal data"""
    foto_category = FotoCategorySerializer(read_only=True)
    foto_category_id = serializers.PrimaryKeyRelatedField(
        queryset=FotoCategory.objects.all(),
        source='foto_category',
        write_only=True
    )
    
    class Meta:
        model = FotoDescription
        fields = [
            'id', 'name', 'author', 'event', 'image', 
            'foto_category', 'foto_category_id', 'created', 'edited'
        ]
        read_only_fields = ['id', 'created', 'edited']


class FotoDescriptionDetailSerializer(serializers.ModelSerializer):
    """Serializer for photo details - full data with tags"""
    foto_category = FotoCategorySerializer(read_only=True)
    foto_category_id = serializers.PrimaryKeyRelatedField(
        queryset=FotoCategory.objects.all(),
        source='foto_category',
        write_only=True
    )
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = FotoDescription
        fields = [
            'id', 'name', 'author', 'event', 'image',
            'foto_category', 'foto_category_id', 'tags',
            'created', 'edited'
        ]
        read_only_fields = ['id', 'created', 'edited']
    
    def get_tags(self, obj):
        # Get all tags related to this photo
        tags = FotoTags.objects.filter(foto_description=obj)
        return [tag.tags for tag in tags]


class FotoTagsSerializer(serializers.ModelSerializer):
    photos = FotoDescriptionListSerializer(source='foto_description', many=True, read_only=True)
    photo_ids = serializers.PrimaryKeyRelatedField(
        queryset=FotoDescription.objects.all(),
        source='foto_description',
        many=True,
        write_only=True
    )
    
    class Meta:
        model = FotoTags
        fields = ['id', 'tags', 'photos', 'photo_ids']
        read_only_fields = ['id']


# Blog Post Serializers
class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for listing blog posts - minimal data"""
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True,
        required=False
    )
    comments_count = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'excerpt', 'slug', 'author', 'author_id',
            'created', 'edited', 'comments_count'
        ]
        read_only_fields = ['id', 'slug', 'created', 'edited']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_excerpt(self, obj):
        """Return first 200 characters of post"""
        return obj.post[:200] + '...' if len(obj.post) > 200 else obj.post


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog post details - full data"""
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True,
        required=False
    )
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'post', 'slug', 'author', 'author_id',
            'created', 'edited', 'comments_count'
        ]
        read_only_fields = ['id', 'slug', 'created', 'edited']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        # Auto-generate slug from title
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        
        # Set author from request user if not provided
        request = self.context.get('request')
        if request and not validated_data.get('author'):
            validated_data['author'] = request.user
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Update slug if title changed
        if 'title' in validated_data and validated_data['title'] != instance.title:
            validated_data['slug'] = slugify(validated_data['title'])
        
        return super().update(instance, validated_data)


class PostCategorySerializer(serializers.ModelSerializer):
    posts = BlogPostListSerializer(source='blog_post', many=True, read_only=True)
    post_ids = serializers.PrimaryKeyRelatedField(
        queryset=BlogPost.objects.all(),
        source='blog_post',
        many=True,
        write_only=True
    )
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PostCategory
        fields = ['id', 'category', 'posts', 'post_ids', 'posts_count']
        read_only_fields = ['id']
    
    def get_posts_count(self, obj):
        return obj.blog_post.count()


class PostCommentsSerializer(serializers.ModelSerializer):
    blog_post_title = serializers.CharField(source='blog_post.title', read_only=True)
    blog_post_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogPost.objects.all(),
        source='blog_post',
        write_only=True
    )
    
    class Meta:
        model = PostComments
        fields = [
            'id', 'blog_post', 'blog_post_id', 'blog_post_title',
            'comment', 'author', 'created', 'edited'
        ]
        read_only_fields = ['id', 'created', 'edited', 'blog_post']
    
    def to_representation(self, instance):
        """Include minimal blog post data in response"""
        representation = super().to_representation(instance)
        representation['blog_post'] = {
            'id': instance.blog_post.id,
            'title': instance.blog_post.title,
            'slug': instance.blog_post.slug,
        }
        return representation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'name', 'email', 'topic', 'message', 'created']
        read_only_fields = ['id', 'created']
    
    def validate_email(self, value):
        """Validate email format"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Podaj prawidłowy adres email")
        return value.lower()
