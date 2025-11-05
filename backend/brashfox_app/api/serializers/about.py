"""
Serializer for AboutMe model.
"""
from rest_framework import serializers
from brashfox_app.models import AboutMe


class AboutMeSerializer(serializers.ModelSerializer):
    """
    Serializer for AboutMe singleton model.
    """
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AboutMe
        fields = [
            'id',
            'title',
            'name',
            'bio',
            'profile_image',
            'profile_image_url',
            'specializations',
            'email',
            'phone',
            'social_links',
            'updated',
            'created',
        ]
        read_only_fields = ['id', 'created', 'updated']
    
    def get_profile_image_url(self, obj):
        """Get full URL for profile image."""
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None
