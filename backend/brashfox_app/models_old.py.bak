from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class FotoCategory(models.Model):
    category = models.CharField(
        max_length=255,
        verbose_name='Kategoria zdjęcia',
    )

    class Meta:
        verbose_name = 'Kategoria zdjęcia'
        verbose_name_plural = 'Kategorie zdjęć'
        ordering = ['category']

    def __str__(self):
        return self.category


class FotoDescription(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Opis zdjęcia',
    )
    author = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name='Autor zdjęcia',
    )
    event = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Z jakiego wydarzenia jest to zdjęcie',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Data powstania opisu',
    )
    edited = models.DateTimeField(
        auto_now=True,
        null=True,
        verbose_name='Data aktualizacji',
    )
    image = models.ImageField(
        upload_to='photos/',
        verbose_name='Zdjęcie',
    )
    foto_category = models.ForeignKey(
        FotoCategory,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Kategoria'
    )

    class Meta:
        verbose_name = 'Opis zdjęcia'
        verbose_name_plural = 'Opisy zdjęć'
        ordering = ['-created']

    def __str__(self):
        return self.name


class FotoTags(models.Model):
    foto_description = models.ManyToManyField(
        FotoDescription,
        related_name='tags',
        verbose_name='Zdjęcia'
    )
    tags = models.CharField(
        max_length=60,
        verbose_name='Tag zdjęcia',
    )

    class Meta:
        verbose_name = 'Tag zdjęcia'
        verbose_name_plural = 'Tagi zdjęć'
        ordering = ['tags']

    def __str__(self):
        return self.tags


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


class Message(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='Imię',
    )
    email = models.EmailField(
        verbose_name='E-mail',
    )
    topic = models.CharField(
        max_length=64,
        verbose_name='Temat',
    )
    message = models.TextField(
        verbose_name='Wiadomość'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data utworzenia'
    )

    class Meta:
        verbose_name = 'Wiadomość'
        verbose_name_plural = 'Wiadomości'
        ordering = ['-created']

    def __str__(self):
        return f'{self.topic} - {self.name}'
