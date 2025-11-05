"""
User and Group ViewSets
"""
from django.contrib.auth.models import Group, User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from brashfox_app.api.serializers import (
    UserSerializer,
    UserCreateSerializer,
    GroupSerializer,
)
from brashfox_app.api.permissions import IsOwnerOrAdmin
from brashfox_app.api.throttles import RegisterThrottle
from brashfox_app.api.services import UserService


class UserViewSet(ModelViewSet):
    """
    API endpoint for users.
    - List/Retrieve: Authenticated users only
    - Create: Anyone (registration) - rate limited to 3/hour
    - Update/Delete: Owner or Admin only
    """
    queryset = User.objects.all().order_by('-date_joined')
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]
    
    def get_throttles(self):
        """Apply stricter rate limiting to registration"""
        if self.action == 'create':
            return [RegisterThrottle()]
        return super().get_throttles()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile with statistics"""
        serializer = self.get_serializer(request.user)
        data = serializer.data
        
        # Add user statistics using service
        data['statistics'] = UserService.get_user_statistics(request.user)
        
        return Response(data)


class GroupViewSet(ModelViewSet):
    """
    API endpoint for groups.
    Requires authentication.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
