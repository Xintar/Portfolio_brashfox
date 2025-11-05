"""
Views package - LEGACY Django template views (SSR)

Modern REST API views are in: brashfox_app/api/views/

Organized by domain:
- common: Index page
- portfolio: Photo gallery and management
- blog: Blog posts and articles
- about: About Me page
- contact: Contact form
- auth: Login, Logout, Register
"""

# Common
from .common import IndexView

# Portfolio
from .portfolio import (
    PortfolioView,
    DetailFotoView,
    AddFotosView,
    EditFotosView,
    DeleteFotosView,
)

# Blog
from .blog import (
    BlogView,
    PostDetailView,
    AddPostView,
    EditPostView,
    DeletePostView,
)

# About
from .about import AboutMeView

# Contact
from .contact import (
    ContactView,
    ContactSucessView,
)

# Auth
from .auth import (
    LoginView,
    LogoutView,
    register,
)


__all__ = [
    # Common
    'IndexView',
    # Portfolio
    'PortfolioView',
    'DetailFotoView',
    'AddFotosView',
    'EditFotosView',
    'DeleteFotosView',
    # Blog
    'BlogView',
    'PostDetailView',
    'AddPostView',
    'EditPostView',
    'DeletePostView',
    # About
    'AboutMeView',
    # Contact
    'ContactView',
    'ContactSucessView',
    # Auth
    'LoginView',
    'LogoutView',
    'register',
]
