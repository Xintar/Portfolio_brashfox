"""
User and Group serializers
"""
from django.contrib.auth.models import Group, User
from rest_framework import serializers


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
