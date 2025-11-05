"""
Message-related ViewSets: Message (contact form)
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from brashfox_app.models import Message
from brashfox_app.api.serializers import MessageSerializer
from brashfox_app.api.throttles import ContactFormThrottle
from brashfox_app.api.services import MessageService


class MessageViewSet(ModelViewSet):
    """
    API endpoint for contact form messages.
    - Create: Anyone (throttled)
    - Read/Update/Delete: Admins only (via permission)
    Throttled to prevent spam (10/hour from same IP).
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    throttle_classes = [ContactFormThrottle]
    ordering_fields = ['created']
    ordering = ['-created']
    
    def get_permissions(self):
        """
        Allow anyone to create messages (contact form),
        but only admins can read/update/delete them
        """
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
