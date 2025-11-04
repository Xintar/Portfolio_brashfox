"""
API Views - Export all ViewSets

This module aggregates all API ViewSets for easy import in urls.py.
Organized by domain:
- User/Auth: UserViewSet, GroupViewSet
- Photos: FotoCategoryViewSet, FotoDescriptionViewSet, FotoTagsViewSet
- Blog: BlogPostViewSet, PostCategoryViewSet
- Comments: PostCommentsViewSet
- Messages: MessageViewSet
"""

# User & Auth
from .user import UserViewSet, GroupViewSet

# Photos
from .photo import (
    FotoCategoryViewSet,
    FotoDescriptionViewSet,
    FotoTagsViewSet,
)

# Blog
from .blog import (
    BlogPostViewSet,
    PostCategoryViewSet,
)

# Comments
from .comment import PostCommentsViewSet

# Messages (Contact Form)
from .message import MessageViewSet


__all__ = [
    # User/Auth
    'UserViewSet',
    'GroupViewSet',
    # Photos
    'FotoCategoryViewSet',
    'FotoDescriptionViewSet',
    'FotoTagsViewSet',
    # Blog
    'BlogPostViewSet',
    'PostCategoryViewSet',
    # Comments
    'PostCommentsViewSet',
    # Messages
    'MessageViewSet',
]
