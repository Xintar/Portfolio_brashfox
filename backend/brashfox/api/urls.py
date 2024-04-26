from django.urls import path, include
from rest_framework.routers import DefaultRouter

from brashfox_app.api.urls import (
    router as brashfox_app_router,
)

router = DefaultRouter()
router.registry.extend(brashfox_app_router.registry)

urlpatterns = [
    path('', include(router.urls)),
]
