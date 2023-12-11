from django.contrib import admin

from brashfox_app.models import (
    BlogPost,
    PostCategory,
    PostComments,
    Message
)

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(PostCategory)
admin.site.register(PostComments)
admin.site.register(Message)