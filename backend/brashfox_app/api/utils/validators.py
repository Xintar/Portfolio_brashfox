"""
Custom Validators

Reusable validation functions for models and serializers.
"""
import os
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import FileUpload, TextValidation, URLPatterns


def validate_image_file(file):
    """
    Validate uploaded image file format and size.
    
    Args:
        file: UploadedFile instance
        
    Raises:
        ValidationError: If file is invalid
    """
    if not file:
        return
    
    # Check file size
    if file.size > FileUpload.MAX_IMAGE_SIZE:
        raise ValidationError(
            _(f'File size exceeds maximum allowed size of {FileUpload.MAX_IMAGE_SIZE / (1024*1024):.0f}MB.')
        )
    
    # Check file extension
    ext = os.path.splitext(file.name)[1].lower().lstrip('.')
    if ext not in FileUpload.ALLOWED_IMAGE_FORMATS:
        raise ValidationError(
            _(f'Invalid file format. Allowed formats: {", ".join(FileUpload.ALLOWED_IMAGE_FORMATS)}')
        )


def validate_avatar_file(file):
    """
    Validate uploaded avatar file (stricter size limit).
    
    Args:
        file: UploadedFile instance
        
    Raises:
        ValidationError: If file is invalid
    """
    if not file:
        return
    
    # Check file size (stricter for avatars)
    if file.size > FileUpload.MAX_AVATAR_SIZE:
        raise ValidationError(
            _(f'Avatar size exceeds maximum allowed size of {FileUpload.MAX_AVATAR_SIZE / (1024*1024):.0f}MB.')
        )
    
    # Check file extension
    ext = os.path.splitext(file.name)[1].lower().lstrip('.')
    if ext not in FileUpload.ALLOWED_IMAGE_FORMATS:
        raise ValidationError(
            _(f'Invalid file format. Allowed formats: {", ".join(FileUpload.ALLOWED_IMAGE_FORMATS)}')
        )


def validate_slug(value):
    """
    Validate slug format.
    
    Args:
        value: String to validate
        
    Raises:
        ValidationError: If slug format is invalid
    """
    if not re.match(URLPatterns.SLUG_PATTERN, value):
        raise ValidationError(
            _('Slug can only contain letters, numbers, hyphens, and underscores.')
        )


def validate_username(value):
    """
    Validate username format.
    
    Args:
        value: String to validate
        
    Raises:
        ValidationError: If username format is invalid
    """
    if len(value) < TextValidation.MIN_USERNAME_LENGTH:
        raise ValidationError(
            _(f'Username must be at least {TextValidation.MIN_USERNAME_LENGTH} characters long.')
        )
    
    if not re.match(URLPatterns.USERNAME_PATTERN, value):
        raise ValidationError(
            _('Username can only contain letters, numbers, and @/./+/-/_ characters.')
        )


def validate_comment_length(value):
    """
    Validate comment text length.
    
    Args:
        value: String to validate
        
    Raises:
        ValidationError: If comment is too short or too long
    """
    cleaned = value.strip()
    
    if len(cleaned) < TextValidation.MIN_COMMENT_LENGTH:
        raise ValidationError(
            _(f'Comment must be at least {TextValidation.MIN_COMMENT_LENGTH} characters long.')
        )
    
    if len(cleaned) > TextValidation.MAX_COMMENT_LENGTH:
        raise ValidationError(
            _(f'Comment cannot exceed {TextValidation.MAX_COMMENT_LENGTH} characters.')
        )


def validate_message_length(value):
    """
    Validate message text length.
    
    Args:
        value: String to validate
        
    Raises:
        ValidationError: If message is too short or too long
    """
    cleaned = value.strip()
    
    if len(cleaned) < TextValidation.MIN_MESSAGE_LENGTH:
        raise ValidationError(
            _(f'Message must be at least {TextValidation.MIN_MESSAGE_LENGTH} characters long.')
        )
    
    if len(cleaned) > TextValidation.MAX_MESSAGE_LENGTH:
        raise ValidationError(
            _(f'Message cannot exceed {TextValidation.MAX_MESSAGE_LENGTH} characters.')
        )


def validate_post_title(value):
    """
    Validate blog post title.
    
    Args:
        value: String to validate
        
    Raises:
        ValidationError: If title is too short or too long
    """
    cleaned = value.strip()
    
    if len(cleaned) < TextValidation.MIN_TITLE_LENGTH:
        raise ValidationError(
            _(f'Title must be at least {TextValidation.MIN_TITLE_LENGTH} characters long.')
        )
    
    if len(cleaned) > TextValidation.MAX_TITLE_LENGTH:
        raise ValidationError(
            _(f'Title cannot exceed {TextValidation.MAX_TITLE_LENGTH} characters.')
        )
