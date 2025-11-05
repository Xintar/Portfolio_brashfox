"""
Comment-related models: PostComments
"""
from django.db import models
from .blog import BlogPost


class PostComments(models.Model):
    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Post'
    )
    comment = models.TextField(
        verbose_name='Komentarz'
    )
    author = models.CharField(
        max_length=255,
        verbose_name='Nazwa komentującego',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Data powstania komentarza',
    )
    edited = models.DateTimeField(
        auto_now=True,
        verbose_name='Data aktualizacji',
    )

    class Meta:
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'
        ordering = ['created']

    def __str__(self):
        return f'Komentarz od {self.author} do "{self.blog_post.title}"'
