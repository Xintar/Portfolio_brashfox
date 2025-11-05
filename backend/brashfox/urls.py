"""
URL configuration for brashfox project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView

from brashfox_app.api.auth_views import (
    ThrottledTokenObtainPairView,
    ThrottledTokenRefreshView,
)
from brashfox_app.views import (
    IndexView,
    PortfolioView,
    AboutMeView,
    ContactView,
    ContactSucessView,
    BlogView,
    PostDetailView,
    AddPostView,
    EditPostView,
    DeletePostView,
    LoginView,
    LogoutView,
    register,
    DetailFotoView,
    AddFotosView,
    EditFotosView,
    DeleteFotosView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('brashfox.api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # JWT Authentication (with rate limiting)
    path('api/token/', ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', ThrottledTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API Documentation
    path('api/schema/', include('brashfox.api.schema_urls')),
    
    # Django Template Views (legacy - można usunąć jeśli używasz tylko React)
    path('', IndexView.as_view(), name='start'),
    path('about-me/', AboutMeView.as_view()),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact-success/', ContactSucessView.as_view(), name='contact-succes'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('post/<str:slug>/', PostDetailView.as_view()),
    path('add-post/', AddPostView.as_view(), name='add-post'),
    path('edit-post/<int:pk>/', EditPostView.as_view(), name='edit-post'),
    path('delete-post/<int:pk>/', DeletePostView.as_view(), name='delete-post'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('fotos/detail/<int:id>/', DetailFotoView.as_view(), name='foto-detail'),
    path('fotos/add/', AddFotosView.as_view(), name='add-fotos'),
    path('fotos/edit/<int:pk>/', EditFotosView.as_view(), name='edit-fotos'),
    path('fotos/delete/<int:pk>/', DeleteFotosView.as_view(), name='delete-fotos'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
