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


# Main router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')

# Photos (renamed from foto_descriptions for better REST naming)
router.register(r'photos', FotoDescriptionViewSet, basename='photo')
router.register(r'photo-categories', FotoCategoryViewSet, basename='photo-category')
router.register(r'photo-tags', FotoTagsViewSet, basename='photo-tag')

# Blog posts
router.register(r'blog-posts', BlogPostViewSet, basename='blog-post')
router.register(r'post-categories', PostCategoryViewSet, basename='post-category')

# Comments (standalone access)
router.register(r'comments', PostCommentsViewSet, basename='comment')

# Contact messages
router.register(r'messages', MessageViewSet, basename='message')


