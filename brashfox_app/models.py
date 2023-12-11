from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class FotoCategory(models.Model):
    category = models.CharField(
        max_length=255,
        verbose_name='Kategoria zdjęcia',
    )


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
        default=timezone.now,
        editable=False,
        verbose_name='Data powstania opisu',
    )
    edited = models.DateTimeField(
        null=True,
        verbose_name='Data aktualizacji',
    )
    image = models.ImageField(upload_to='./static/images/portfolio')
    foto_category = models.ForeignKey(FotoCategory, on_delete=models.CASCADE)


class FotoTags(models.Model):
    foto_description = models.ManyToManyField(FotoDescription)
    tags = models.CharField(
        max_length=60,
        verbose_name='Tag zdjęcia',
    )


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
        default=timezone.now,
        editable=False,
        verbose_name='Data powstania wpisu',
    )
    edited = models.DateTimeField(
        null=True,
        verbose_name='Data aktualizacji wpisu',
    )
    slug = models.SlugField(
        max_length=255,
    )


class PostCategory(models.Model):
    category = models.CharField(
        max_length=255,
        verbose_name='Kategoria wpisu na blogu'
    )
    blog_post = models.ManyToManyField(BlogPost)


class PostComments(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.CharField(
        max_length=255,
        verbose_name='Nazwa komentującego',

    )
    created = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name='Data powstania komnentarza',
    )
    edited = models.DateTimeField(
        null=True,
        verbose_name='Data aktualizacji edycji',
    )


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
        default=timezone.now
    )