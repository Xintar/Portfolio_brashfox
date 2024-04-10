from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class FotoCategory(models.Model):
    category = models.CharField(
        max_length=255,
        verbose_name='Kategoria zdjęcia',
    )

    def __str__(self):
        return self.category


class FotoDescription(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Opis zdjęcia',
    )
    author = models.CharField(
        null=True,
        max_length=255,
        verbose_name='Autor zdjęcia',
    )
    ivent = models.CharField(
        max_length=255,
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
        upload_to='./static/images/portfolio',
        verbose_name='Zdjęcie',
    )
    foto_category = models.ForeignKey(FotoCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FotoTags(models.Model):
    foto_description = models.ManyToManyField(FotoDescription)
    tags = models.CharField(
        max_length=60,
        verbose_name='Tag zdjęcia',
    )

    def __str__(self):
        return self.tags


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=255,
        verbose_name='Tytuł wpisu',
    )
    post = models.TextField(
        verbose_name='Treś wpisu',
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
    )

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    category = models.CharField(
        max_length=255,
        verbose_name='Kategoria wpisu na blogu'
    )
    blog_post = models.ManyToManyField(BlogPost)

    def __str__(self):
        return self.category


class PostComments(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.TextField(
        verbose_name='Komentarza'
    )
    author = models.CharField(
        max_length=255,
        verbose_name='Nazwa komentującego',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Data powstania komnentarza',
    )
    edited = models.DateTimeField(
        auto_now=True,
        verbose_name='Data aktualizacji edycji',
    )

    def __str__(self):
        return self.comment


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
        auto_now_add=True
    )

    def __str__(self):
        return self.topic
