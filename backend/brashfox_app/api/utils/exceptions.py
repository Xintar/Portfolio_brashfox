"""
Custom Exceptions

Application-specific exceptions for better error handling.
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class BusinessLogicError(APIException):
    """
    Base exception for business logic errors.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A business logic error occurred.'
    default_code = 'business_logic_error'


class ResourceNotFoundError(APIException):
    """
    Exception raised when a resource is not found.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'The requested resource was not found.'
    default_code = 'resource_not_found'


class DuplicateResourceError(APIException):
    """
    Exception raised when attempting to create a duplicate resource.
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'A resource with these details already exists.'
    default_code = 'duplicate_resource'


class InvalidFileError(APIException):
    """
    Exception raised when uploaded file is invalid.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The uploaded file is invalid.'
    default_code = 'invalid_file'


class FileTooLargeError(APIException):
    """
    Exception raised when uploaded file exceeds size limit.
    """
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    default_detail = 'The uploaded file is too large.'
    default_code = 'file_too_large'


class PermissionDeniedError(APIException):
    """
    Exception raised when user lacks required permissions.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'permission_denied'


class RateLimitExceededError(APIException):
    """
    Exception raised when rate limit is exceeded.
    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Request rate limit exceeded. Please try again later.'
    default_code = 'rate_limit_exceeded'


class ValidationError(APIException):
    """
    Exception raised for validation errors.
    """
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Validation failed.'
    default_code = 'validation_error'
    
    def __init__(self, detail=None, field_errors=None):
        """
        Initialize with optional field-specific errors.
        
        Args:
            detail: General error message
            field_errors: Dict of field-specific errors
        """
        if field_errors:
            detail = field_errors
        super().__init__(detail)


class ServiceUnavailableError(APIException):
    """
    Exception raised when a service is temporarily unavailable.
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service temporarily unavailable. Please try again later.'
    default_code = 'service_unavailable'
