from rest_framework.routers import DefaultRouter

from brashfox_app.api.views import (
    BlogPostViewSet,
)


post_router = DefaultRouter()
post_router.register(r'posts', BlogPostViewSet)
