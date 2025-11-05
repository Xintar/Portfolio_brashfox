from django.contrib import admin

from brashfox_app.models import (
    BlogPost,
    PostCategory,
    PostComments,
    Message,
    FotoDescription,
    FotoCategory,
    FotoTags,
    AboutMe,
)


# Register models
admin.site.register(BlogPost)
admin.site.register(PostCategory)
admin.site.register(PostComments)
admin.site.register(Message)
admin.site.register(FotoDescription)
admin.site.register(FotoCategory)
admin.site.register(FotoTags)


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    """
    Admin for AboutMe singleton model.
    """
    list_display = ['name', 'title', 'email', 'phone', 'updated']
    readonly_fields = ['created', 'updated']
    
    def has_add_permission(self, request):
        """Only allow one instance."""
        if AboutMe.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton."""
        return False

