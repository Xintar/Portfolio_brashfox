from rest_framework.routers import DefaultRouter

from brashfox_app.api.views import (
    BlogPostViewSet,
    UserViewSet,
    GroupViewSet,
)


post_router = DefaultRouter()

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'posts', BlogPostViewSet)