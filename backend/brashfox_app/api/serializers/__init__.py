"""
API Serializers package - organized by domain
"""
# User serializers
from .user import (
    UserSerializer,
    UserCreateSerializer,
    GroupSerializer,
)

# Photo serializers
from .photo import (
    FotoCategorySerializer,
    FotoDescriptionListSerializer,
    FotoDescriptionDetailSerializer,
    FotoTagsSerializer,
)

# Blog serializers
from .blog import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    PostCategorySerializer,
)

# Comment serializers
from .comment import PostCommentsSerializer

# Message serializers
from .message import MessageSerializer

# Export all serializers
__all__ = [
    # User
    'UserSerializer',
    'UserCreateSerializer',
    'GroupSerializer',
    # Photo
    'FotoCategorySerializer',
    'FotoDescriptionListSerializer',
    'FotoDescriptionDetailSerializer',
    'FotoTagsSerializer',
    # Blog
    'BlogPostListSerializer',
    'BlogPostDetailSerializer',
    'PostCategorySerializer',
    # Comment
    'PostCommentsSerializer',
    # Message
    'MessageSerializer',
]
