"""
Application Constants

Centralized location for all application-wide constants.
"""

# File Upload Settings
class FileUpload:
    """Constants for file uploads"""
    
    # Image formats
    ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    
    # File size limits (in bytes)
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_AVATAR_SIZE = 2 * 1024 * 1024  # 2MB
    
    # Image dimensions
    MAX_IMAGE_WIDTH = 4000
    MAX_IMAGE_HEIGHT = 4000
    THUMBNAIL_SIZE = (300, 300)


# Text Validation
class TextValidation:
    """Constants for text validation"""
    
    # Comment limits
    MIN_COMMENT_LENGTH = 10
    MAX_COMMENT_LENGTH = 1000
    
    # Message limits
    MIN_MESSAGE_LENGTH = 10
    MAX_MESSAGE_LENGTH = 5000
    
    # Blog post limits
    MIN_TITLE_LENGTH = 5
    MAX_TITLE_LENGTH = 200
    MIN_POST_LENGTH = 50
    MAX_POST_LENGTH = 50000
    
    # Username limits
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 150


# API Settings
class API:
    """API-related constants"""
    
    # Pagination
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    
    # Throttle rates
    ANON_RATE = '100/hour'
    USER_RATE = '1000/hour'
    REGISTER_RATE = '3/hour'
    CONTACT_RATE = '10/hour'
    
    # Cache timeouts (in seconds)
    CACHE_SHORT = 60 * 5  # 5 minutes
    CACHE_MEDIUM = 60 * 30  # 30 minutes
    CACHE_LONG = 60 * 60 * 24  # 24 hours


# Model Defaults
class Defaults:
    """Default values for models"""
    
    DEFAULT_AUTHOR = 'Anonymous'
    DEFAULT_CATEGORY = 'Uncategorized'
    DEFAULT_TAG = 'untagged'


# Status Codes and Messages
class Messages:
    """User-facing messages"""
    
    # Success messages
    SUCCESS_CREATED = 'Successfully created.'
    SUCCESS_UPDATED = 'Successfully updated.'
    SUCCESS_DELETED = 'Successfully deleted.'
    
    # Error messages
    ERROR_NOT_FOUND = 'Resource not found.'
    ERROR_PERMISSION = 'You do not have permission to perform this action.'
    ERROR_INVALID_DATA = 'Invalid data provided.'
    ERROR_FILE_TOO_LARGE = 'File size exceeds maximum allowed size.'
    ERROR_INVALID_FORMAT = 'Invalid file format.'
    
    # Validation messages
    VALIDATION_REQUIRED = 'This field is required.'
    VALIDATION_UNIQUE = 'This value must be unique.'
    VALIDATION_MIN_LENGTH = 'Ensure this field has at least {min} characters.'
    VALIDATION_MAX_LENGTH = 'Ensure this field has no more than {max} characters.'


# URL Patterns
class URLPatterns:
    """URL pattern constants"""
    
    # Regex patterns
    SLUG_PATTERN = r'^[-a-zA-Z0-9_]+$'
    USERNAME_PATTERN = r'^[\w.@+-]+$'
    TAG_PATTERN = r'^[a-zA-Z0-9-_]+$'
