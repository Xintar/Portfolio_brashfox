"""
Blog-related models: BlogPost, PostCategory
"""
from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='Autor'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Tytuł wpisu',
    )
    post = models.TextField(
        verbose_name='Treść wpisu',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Data powstania wpisu',
    )
    edited = models.DateTimeField(
        auto_now=True,
        verbose_name='Data aktualizacji wpisu',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Slug',
    )

    class Meta:
        verbose_name = 'Post blogowy'
        verbose_name_plural = 'Posty blogowe'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    category = models.CharField(
        max_length=255,
        verbose_name='Kategoria wpisu na blogu'
    )
    blog_post = models.ManyToManyField(
        BlogPost,
        related_name='categories',
        verbose_name='Posty'
    )

    class Meta:
        verbose_name = 'Kategoria posta'
        verbose_name_plural = 'Kategorie postów'
        ordering = ['category']

    def __str__(self):
        return self.category
