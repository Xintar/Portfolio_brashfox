"""
Blog-related serializers: BlogPost, PostCategory
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.text import slugify
from brashfox_app.models import BlogPost, PostCategory
from .user import UserSerializer


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
