from rest_framework.routers import DefaultRouter

from brashfox_app.api.views import (
    UserViewSet,
    GroupViewSet,
    FotoCategoryViewSet,
    FotoDescriptionViewSet,
    FotoTagsViewSet,
    BlogPostViewSet,
    PostCategoryViewSet,
    PostCommentsViewSet,
    MessageViewSet,
)


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'foto_categories', FotoCategoryViewSet)
router.register(r'foto_descriptions', FotoDescriptionViewSet)
router.register(r'foto_tags', FotoTagsViewSet)
router.register(r'posts', BlogPostViewSet)
router.register(r'post_categories', PostCategoryViewSet)
router.register(r'post_comments', PostCommentsViewSet)
router.register(r'messages', MessageViewSet)
