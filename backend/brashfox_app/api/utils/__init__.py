"""
API Utils - Export all utility modules

This module aggregates all utility functions, validators, constants, and exceptions.

Usage:
    from brashfox_app.api.utils import constants, validators, helpers, exceptions
    
    # Or import specific items:
    from brashfox_app.api.utils.constants import FileUpload, API
    from brashfox_app.api.utils.validators import validate_image_file
    from brashfox_app.api.utils.helpers import generate_unique_filename
    from brashfox_app.api.utils.exceptions import BusinessLogicError
"""

from . import constants
from . import validators
from . import helpers
from . import exceptions

# Export commonly used items
from .constants import (
    FileUpload,
    TextValidation,
    API,
    Defaults,
    Messages,
    URLPatterns,
)

from .validators import (
    validate_image_file,
    validate_avatar_file,
    validate_slug,
    validate_username,
    validate_comment_length,
    validate_message_length,
    validate_post_title,
)

from .helpers import (
    generate_unique_filename,
    generate_photo_path,
    truncate_text,
    generate_excerpt,
    format_file_size,
    sanitize_filename,
    get_client_ip,
    generate_unique_slug,
)

from .exceptions import (
    BusinessLogicError,
    ResourceNotFoundError,
    DuplicateResourceError,
    InvalidFileError,
    FileTooLargeError,
    PermissionDeniedError,
    RateLimitExceededError,
    ValidationError,
    ServiceUnavailableError,
)


__all__ = [
    # Modules
    'constants',
    'validators',
    'helpers',
    'exceptions',
    
    # Constants
    'FileUpload',
    'TextValidation',
    'API',
    'Defaults',
    'Messages',
    'URLPatterns',
    
    # Validators
    'validate_image_file',
    'validate_avatar_file',
    'validate_slug',
    'validate_username',
    'validate_comment_length',
    'validate_message_length',
    'validate_post_title',
    
    # Helpers
    'generate_unique_filename',
    'generate_photo_path',
    'truncate_text',
    'generate_excerpt',
    'format_file_size',
    'sanitize_filename',
    'get_client_ip',
    'generate_unique_slug',
    
    # Exceptions
    'BusinessLogicError',
    'ResourceNotFoundError',
    'DuplicateResourceError',
    'InvalidFileError',
    'FileTooLargeError',
    'PermissionDeniedError',
    'RateLimitExceededError',
    'ValidationError',
    'ServiceUnavailableError',
]
