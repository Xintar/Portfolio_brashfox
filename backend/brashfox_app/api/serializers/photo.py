"""
Photo-related serializers: FotoCategory, FotoDescription, FotoTags
"""
from rest_framework import serializers
from brashfox_app.models import FotoCategory, FotoDescription, FotoTags


class FotoCategorySerializer(serializers.ModelSerializer):
    photos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = FotoCategory
        fields = ['id', 'category', 'photos_count']
        read_only_fields = ['id']
    
    def get_photos_count(self, obj):
        return obj.photos.count()


class FotoDescriptionListSerializer(serializers.ModelSerializer):
    """Serializer for listing photos - minimal data"""
    foto_category = FotoCategorySerializer(read_only=True)
    foto_category_id = serializers.PrimaryKeyRelatedField(
        queryset=FotoCategory.objects.all(),
        source='foto_category',
        write_only=True
    )
    
    class Meta:
        model = FotoDescription
        fields = [
            'id', 'name', 'author', 'event', 'image', 
            'foto_category', 'foto_category_id', 'created', 'edited'
        ]
        read_only_fields = ['id', 'created', 'edited']


class FotoDescriptionDetailSerializer(serializers.ModelSerializer):
    """Serializer for photo details - full data with tags"""
    foto_category = FotoCategorySerializer(read_only=True)
    foto_category_id = serializers.PrimaryKeyRelatedField(
        queryset=FotoCategory.objects.all(),
        source='foto_category',
        write_only=True
    )
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = FotoDescription
        fields = [
            'id', 'name', 'author', 'event', 'image',
            'foto_category', 'foto_category_id', 'tags',
            'created', 'edited'
        ]
        read_only_fields = ['id', 'created', 'edited']
    
    def get_tags(self, obj):
        # Get all tags related to this photo
        tags = FotoTags.objects.filter(foto_description=obj)
        return [tag.tags for tag in tags]


class FotoTagsSerializer(serializers.ModelSerializer):
    photos = FotoDescriptionListSerializer(source='foto_description', many=True, read_only=True)
    photo_ids = serializers.PrimaryKeyRelatedField(
        queryset=FotoDescription.objects.all(),
        source='foto_description',
        many=True,
        write_only=True
    )
    
    class Meta:
        model = FotoTags
        fields = ['id', 'tags', 'photos', 'photo_ids']
        read_only_fields = ['id']
