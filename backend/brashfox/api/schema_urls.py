from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # OpenAPI 3.0 Schema
    path('', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI - Interactive API documentation
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # ReDoc - Alternative documentation UI
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
