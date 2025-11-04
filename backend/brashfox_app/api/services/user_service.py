"""
User Service - Business logic for user management
"""
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.exceptions import ValidationError


class UserService:
    """
    Handles user-related business logic:
    - User registration with validation
    - Profile updates
    - User statistics
    """
    
    @staticmethod
    def create_user(validated_data):
        """
        Create a new user with proper password hashing.
        
        Args:
            validated_data: Dictionary with user data (username, email, password)
            
        Returns:
            User instance
            
        Raises:
            ValidationError: If username or email already exists
        """
        username = validated_data.get('username')
        email = validated_data.get('email')
        
        # Check for existing user
        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'User with this username already exists.'})
        
        if email and User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'User with this email already exists.'})
        
        # Create user with hashed password
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
            )
        
        return user
    
    @staticmethod
    def update_user(user, validated_data):
        """
        Update user profile.
        
        Args:
            user: User instance to update
            validated_data: Dictionary with updated data
            
        Returns:
            Updated user instance
        """
        # Don't allow username changes
        validated_data.pop('username', None)
        
        # Handle password separately
        password = validated_data.pop('password', None)
        
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(user, attr, value)
            
            if password:
                user.set_password(password)
            
            user.save()
        
        return user
    
    @staticmethod
    def get_user_statistics(user):
        """
        Get user activity statistics.
        
        Args:
            user: User instance
            
        Returns:
            Dictionary with statistics
        """
        from brashfox_app.models import BlogPost, PostComments, FotoDescription
        
        return {
            'blog_posts_count': BlogPost.objects.filter(author=user).count(),
            'comments_count': PostComments.objects.filter(author=user).count(),
            'photos_count': FotoDescription.objects.filter(author=user.username).count(),
        }
