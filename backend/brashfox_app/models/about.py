"""
About Me model - information about the makeup artist.
"""
from django.db import models
from django.core.exceptions import ValidationError


class AboutMe(models.Model):
    """
    Singleton model for 'About Me' page content.
    Only one instance should exist.
    """
    title = models.CharField(
        max_length=200,
        default="O mnie",
        verbose_name='Tytuł strony',
        help_text="Page title"
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name='Imię/Pseudonim',
        help_text="Artist name or pseudonym"
    )
    
    bio = models.TextField(
        verbose_name='Biografia',
        help_text="Biography/description (supports line breaks)"
    )
    
    profile_image = models.ImageField(
        upload_to='about/',
        verbose_name='Zdjęcie profilowe',
        help_text="Profile photo (recommended: 800x800px, max 5MB)"
    )
    
    specializations = models.JSONField(
        default=list,
        verbose_name='Specjalizacje',
        help_text="List of specializations",
        blank=True
    )
    
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email kontaktowy',
        help_text="Contact email (optional)"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefon kontaktowy',
        help_text="Contact phone (optional)"
    )
    
    social_links = models.JSONField(
        default=dict,
        verbose_name='Linki do mediów społecznościowych',
        help_text="Social media links (e.g., {'instagram': 'url', 'facebook': 'url'})",
        blank=True
    )
    
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Data aktualizacji'
    )
    
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data utworzenia'
    )
    
    class Meta:
        verbose_name = "O mnie"
        verbose_name_plural = "O mnie"
    
    def __str__(self):
        return f"About: {self.name}"
    
    def save(self, *args, **kwargs):
        """Ensure only one instance exists (singleton pattern)."""
        if not self.pk and AboutMe.objects.exists():
            raise ValidationError("Może istnieć tylko jedna instancja 'O mnie'. Edytuj istniejącą.")
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance or None if it doesn't exist."""
        return cls.objects.first()
