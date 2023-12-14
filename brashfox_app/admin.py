from django.contrib import admin

from brashfox_app.models import (
    BlogPost,
    PostCategory,
    PostComments,
    Message,
    FotoDescription,
    FotoCategory,
    FotoTags
)

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(PostCategory)
admin.site.register(PostComments)
admin.site.register(Message)
admin.site.register(FotoDescription)
admin.site.register(FotoCategory)
admin.site.register(FotoTags)
