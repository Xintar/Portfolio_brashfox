"""
Comment-related serializers: PostComments
"""
from rest_framework import serializers
from brashfox_app.models import BlogPost, PostComments


class PostCommentsSerializer(serializers.ModelSerializer):
    blog_post_title = serializers.CharField(source='blog_post.title', read_only=True)
    blog_post_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogPost.objects.all(),
        source='blog_post',
        write_only=True
    )
    
    class Meta:
        model = PostComments
        fields = [
            'id', 'blog_post', 'blog_post_id', 'blog_post_title',
            'comment', 'author', 'created', 'edited'
        ]
        read_only_fields = ['id', 'created', 'edited', 'blog_post']
    
    def to_representation(self, instance):
        """Include minimal blog post data in response"""
        representation = super().to_representation(instance)
        representation['blog_post'] = {
            'id': instance.blog_post.id,
            'title': instance.blog_post.title,
            'slug': instance.blog_post.slug,
        }
        return representation
