"""
Photo-related ViewSets: FotoCategory, FotoDescription, FotoTags
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from brashfox_app.models import (
    FotoCategory,
    FotoDescription,
    FotoTags,
)
from brashfox_app.api.serializers import (
    FotoCategorySerializer,
    FotoDescriptionListSerializer,
    FotoDescriptionDetailSerializer,
    FotoTagsSerializer,
)
from brashfox_app.api.permissions import (
    IsAuthorOrReadOnly,
    IsAdminOrReadOnly,
)
from brashfox_app.api.services import PhotoService


class FotoCategoryViewSet(ModelViewSet):
    """
    API endpoint for photo categories.
    - Read: Anyone
    - Write: Admins only
    """
    queryset = FotoCategory.objects.all()
    serializer_class = FotoCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    

class FotoDescriptionViewSet(ModelViewSet):
    """
    API endpoint for photos.
    - Read: Anyone
    - Create: Authenticated users
    - Update/Delete: Author or Admin only
    Uses different serializers for list and detail views.
    Automatically sets author to current user on create.
    """
    queryset = FotoDescription.objects.select_related('foto_category').all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_fields = ['foto_category', 'author']
    search_fields = ['name', 'author', 'event']
    ordering_fields = ['created', 'edited', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FotoDescriptionDetailSerializer
        return FotoDescriptionListSerializer
    
    def perform_create(self, serializer):
        """Automatically set author to current user"""
        serializer.save(author=self.request.user.username)
    

class FotoTagsViewSet(ModelViewSet):
    """
    API endpoint for photo tags.
    - Read: Anyone
    - Write: Authenticated users only
    """
    queryset = FotoTags.objects.prefetch_related('foto_description').all()
    serializer_class = FotoTagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['tags']
    ordering_fields = ['tags']
