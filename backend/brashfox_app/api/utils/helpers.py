"""
Helper Functions

Utility functions used across the application.
"""
import os
import uuid
from datetime import datetime
from django.utils.text import slugify
from django.utils import timezone


def generate_unique_filename(instance, filename):
    """
    Generate a unique filename for uploaded files.
    
    Args:
        instance: Model instance
        filename: Original filename
        
    Returns:
        String path for the file
        
    Example:
        'uploads/2024/11/abc123-original-name.jpg'
    """
    ext = os.path.splitext(filename)[1].lower()
    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(filename)[0]
    safe_name = slugify(base_name)[:30]  # Limit length
    
    new_filename = f"{timestamp}_{unique_id}_{safe_name}{ext}"
    
    # Organize by year/month
    upload_date = timezone.now()
    return f"uploads/{upload_date.year}/{upload_date.month:02d}/{new_filename}"


def generate_photo_path(instance, filename):
    """
    Generate path for photo uploads.
    
    Args:
        instance: FotoDescription instance
        filename: Original filename
        
    Returns:
        String path like 'photos/2024/11/unique-name.jpg'
    """
    ext = os.path.splitext(filename)[1].lower()
    unique_id = uuid.uuid4().hex[:8]
    safe_name = slugify(os.path.splitext(filename)[0])[:30]
    
    upload_date = timezone.now()
    return f"photos/{upload_date.year}/{upload_date.month:02d}/{unique_id}_{safe_name}{ext}"


def truncate_text(text, max_length=200, suffix='...'):
    """
    Truncate text to specified length with suffix.
    
    Args:
        text: String to truncate
        max_length: Maximum length (default 200)
        suffix: Suffix to add if truncated (default '...')
        
    Returns:
        Truncated string
        
    Example:
        truncate_text('Long text here', 10) -> 'Long te...'
    """
    if not text:
        return ''
    
    text = text.strip()
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].rstrip() + suffix


def generate_excerpt(text, max_length=200):
    """
    Generate excerpt from text (truncate at word boundary).
    
    Args:
        text: String to create excerpt from
        max_length: Maximum length (default 200)
        
    Returns:
        Excerpt string
    """
    if not text or len(text) <= max_length:
        return text
    
    # Truncate at word boundary
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated.rstrip('.,;:!?') + '...'


def format_file_size(size_bytes):
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string like '1.5 MB'
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def sanitize_filename(filename):
    """
    Sanitize filename by removing unsafe characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Keep extension
    name, ext = os.path.splitext(filename)
    
    # Slugify name part
    safe_name = slugify(name)
    
    # If slugify removes everything, use a default
    if not safe_name:
        safe_name = 'file'
    
    return f"{safe_name}{ext.lower()}"


def get_client_ip(request):
    """
    Get client IP address from request.
    
    Args:
        request: Django request object
        
    Returns:
        IP address string
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_unique_slug(model_class, base_slug, instance_id=None):
    """
    Generate a unique slug for a model.
    
    Args:
        model_class: Django model class
        base_slug: Base slug to start from
        instance_id: ID of instance being updated (to exclude from uniqueness check)
        
    Returns:
        Unique slug string
    """
    slug = base_slug
    counter = 1
    
    while True:
        # Check if slug exists (excluding current instance if updating)
        queryset = model_class.objects.filter(slug=slug)
        if instance_id:
            queryset = queryset.exclude(id=instance_id)
        
        if not queryset.exists():
            return slug
        
        # Append counter and try again
        slug = f"{base_slug}-{counter}"
        counter += 1
