"""
About Me API view.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from brashfox_app.models import AboutMe
from brashfox_app.api.serializers import AboutMeSerializer


class AboutMeView(APIView):
    """
    Retrieve the AboutMe singleton instance.
    Public endpoint - no authentication required.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get AboutMe data."""
        about = AboutMe.get_instance()
        
        if not about:
            return Response(
                {'detail': 'About Me content not found. Please create it in admin panel.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AboutMeSerializer(about, context={'request': request})
        return Response(serializer.data)
