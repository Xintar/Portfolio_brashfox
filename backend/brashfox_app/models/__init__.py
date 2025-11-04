"""
Models package - organized by domain
"""
# Photo models
from .photo import FotoCategory, FotoDescription, FotoTags

# Blog models
from .blog import BlogPost, PostCategory

# Comment models
from .comment import PostComments

# Message models
from .message import Message

# Export all models
__all__ = [
    # Photo
    'FotoCategory',
    'FotoDescription',
    'FotoTags',
    # Blog
    'BlogPost',
    'PostCategory',
    # Comment
    'PostComments',
    # Message
    'Message',
]
