"""
Photo-related models: FotoCategory, FotoDescription, FotoTags
"""
from django.db import models


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
