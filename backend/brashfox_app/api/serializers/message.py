"""
Contact message serializers: Message
"""
from rest_framework import serializers
from brashfox_app.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'name', 'email', 'topic', 'message', 'created']
        read_only_fields = ['id', 'created']
    
    def validate_email(self, value):
        """Validate email format"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Podaj prawidłowy adres email")
        return value.lower()
