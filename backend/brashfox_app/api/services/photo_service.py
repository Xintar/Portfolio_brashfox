"""
Photo Service - Business logic for photo management
"""
from django.db import transaction

from brashfox_app.models import FotoDescription, FotoCategory
from brashfox_app.api.utils.validators import validate_image_file


class PhotoService:
    """
    Handles photo-related business logic:
    - Photo upload validation
    - Image processing
    - Photo metadata management
    """
    
    @staticmethod
    def validate_image(image_file):
        """
        Validate uploaded image file.
        
        Args:
            image_file: UploadedFile instance
            
        Raises:
            ValidationError: If file is invalid
        """
        # Use centralized validator
        validate_image_file(image_file)
    
    @staticmethod
    def create_photo(author, validated_data):
        """
        Create a new photo with validation.
        
        Args:
            author: User instance or username string
            validated_data: Dictionary with photo data
            
        Returns:
            FotoDescription instance
        """
        image = validated_data.get('image')
        
        # Validate image
        PhotoService.validate_image(image)
        
        # Get author username
        author_username = author.username if hasattr(author, 'username') else str(author)
        
        with transaction.atomic():
            photo = FotoDescription.objects.create(
                author=author_username,
                **validated_data
            )
        
        return photo
    
    @staticmethod
    def update_photo(photo, validated_data):
        """
        Update existing photo.
        
        Args:
            photo: FotoDescription instance
            validated_data: Dictionary with updated data
            
        Returns:
            Updated FotoDescription instance
        """
        new_image = validated_data.get('image')
        
        # Validate new image if provided
        if new_image:
            PhotoService.validate_image(new_image)
        
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(photo, attr, value)
            photo.save()
        
        return photo
    
    @staticmethod
    def get_photos_by_category(category_id):
        """
        Get all photos in a category.
        
        Args:
            category_id: FotoCategory ID
            
        Returns:
            QuerySet of FotoDescription
        """
        return FotoDescription.objects.filter(
            foto_category_id=category_id
        ).select_related('foto_category').order_by('-created')
    
    @staticmethod
    def get_photos_by_tag(tag_name):
        """
        Get all photos with a specific tag.
        
        Args:
            tag_name: Tag name
            
        Returns:
            QuerySet of FotoDescription
        """
        return FotoDescription.objects.filter(
            foto_tags__tags__icontains=tag_name
        ).select_related('foto_category').order_by('-created')
