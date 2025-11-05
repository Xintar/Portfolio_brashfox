"""
Blog Service - Business logic for blog posts
"""
from django.db import transaction
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from brashfox_app.models import BlogPost, PostComments
from brashfox_app.api.utils.helpers import generate_unique_slug
from brashfox_app.api.utils.validators import validate_comment_length


class BlogPostService:
    """
    Handles blog post-related business logic:
    - Post creation with auto-slug generation
    - Post updates with slug validation
    - Comment management
    """
    
    @staticmethod
    def create_post(author, validated_data):
        """
        Create a new blog post with auto-generated slug.
        
        Args:
            author: User instance (post author)
            validated_data: Dictionary with post data
            
        Returns:
            BlogPost instance
            
        Raises:
            ValidationError: If slug already exists
        """
        title = validated_data.get('title')
        slug = validated_data.get('slug')
        
        # Auto-generate slug if not provided
        if not slug:
            slug = slugify(title)
        
        # Ensure slug uniqueness using helper
        slug = generate_unique_slug(BlogPost, slug)
        
        validated_data['slug'] = slug
        
        with transaction.atomic():
            post = BlogPost.objects.create(
                author=author,
                **validated_data
            )
        
        return post
    
    @staticmethod
    def update_post(post, validated_data):
        """
        Update existing blog post.
        
        Args:
            post: BlogPost instance to update
            validated_data: Dictionary with updated data
            
        Returns:
            Updated BlogPost instance
        """
        # Don't allow slug changes to existing post
        validated_data.pop('slug', None)
        
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(post, attr, value)
            post.save()
        
        return post
    
    @staticmethod
    def get_post_comments(post):
        """
        Get all comments for a blog post, ordered by creation date.
        
        Args:
            post: BlogPost instance
            
        Returns:
            QuerySet of PostComments
        """
        return post.comments.select_related('author').order_by('-created')


class CommentService:
    """
    Handles comment-related business logic:
    - Comment creation
    - Comment validation
    """
    
    @staticmethod
    def create_comment(author, blog_post, comment_text):
        """
        Create a new comment on a blog post.
        
        Args:
            author: User instance
            blog_post: BlogPost instance
            comment_text: Comment content
            
        Returns:
            PostComments instance
            
        Raises:
            ValidationError: If comment is empty or too long
        """
        # Validate using centralized validator
        validate_comment_length(comment_text)
        
        with transaction.atomic():
            comment = PostComments.objects.create(
                author=author,
                blog_post=blog_post,
                comment=comment_text.strip()
            )
        
        return comment
