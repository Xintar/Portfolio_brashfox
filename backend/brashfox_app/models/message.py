"""
Contact message model: Message
"""
from django.db import models


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
