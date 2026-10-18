from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from brashfox_app.models import (
    BlogPost,
    PostCategory,
    PostComments,
    Message,
    FotoDescription,
    FotoCategory,
    FotoTags,
    AboutMe,
)
from brashfox_app.models.about import SOCIAL_PLATFORM_CHOICES


# Register models
admin.site.register(BlogPost)
admin.site.register(PostCategory)
admin.site.register(PostComments)
admin.site.register(Message)
admin.site.register(FotoDescription)
admin.site.register(FotoCategory)
admin.site.register(FotoTags)


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    """
    Admin for AboutMe singleton model.
    """
    class SocialLinksForm(forms.ModelForm):
        class Meta:
            model = AboutMe
            fields = (
                'title',
                'name',
                'bio',
                'profile_image',
                'specializations',
                'email',
                'phone',
            )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            saved_links = self.instance.social_links if self.instance and isinstance(
                self.instance.social_links, dict
            ) else {}

            for platform, label in SOCIAL_PLATFORM_CHOICES:
                saved_link = saved_links.get(platform, '')
                if isinstance(saved_link, dict):
                    url = saved_link.get('url', '')
                    enabled = saved_link.get('enabled', False)
                else:
                    url = saved_link
                    enabled = bool(url)

                self.initial[f'{platform}_enabled'] = enabled
                self.initial[f'{platform}_url'] = url

        def clean(self):
            cleaned_data = super().clean()
            social_links = {}

            for platform, label in SOCIAL_PLATFORM_CHOICES:
                enabled = cleaned_data.get(f'{platform}_enabled', False)
                url = (cleaned_data.get(f'{platform}_url') or '').strip()

                if enabled and not url:
                    self.add_error(
                        f'{platform}_url',
                        ValidationError(
                            f'Podaj link do profilu {label}, aby go wyświetlić.',
                            code='required',
                        ),
                    )

                if enabled or url:
                    social_links[platform] = {
                        'enabled': enabled,
                        'url': url,
                    }

            cleaned_data['social_links'] = social_links
            return cleaned_data

        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.social_links = self.cleaned_data['social_links']
            if commit:
                instance.save()
                self.save_m2m()
            return instance

    for platform, label in SOCIAL_PLATFORM_CHOICES:
        enabled_field = forms.BooleanField(
            required=False,
            label=f'Pokaż {label}',
        )
        url_field = forms.URLField(
            required=False,
            label=f'Link {label}',
            widget=forms.URLInput(attrs={'placeholder': 'https://'}),
        )
        SocialLinksForm.base_fields[f'{platform}_enabled'] = enabled_field
        SocialLinksForm.declared_fields[f'{platform}_enabled'] = enabled_field
        SocialLinksForm.base_fields[f'{platform}_url'] = url_field
        SocialLinksForm.declared_fields[f'{platform}_url'] = url_field

    form = SocialLinksForm
    list_display = ['name', 'title', 'email', 'phone', 'updated']
    readonly_fields = ['created', 'updated']
    fieldsets = [
        ('Informacje o profilu', {
            'fields': ('title', 'name', 'bio', 'profile_image', 'specializations'),
        }),
        ('Dane kontaktowe', {
            'fields': ('email', 'phone'),
        }),
        ('Media społecznościowe', {
            'description': (
                'Wpisz adres profilu i zaznacz pole „Pokaż”, aby wyświetlić link '
                'w stopce strony.'
            ),
            'fields': tuple(
                field
                for platform, _ in SOCIAL_PLATFORM_CHOICES
                for field in (f'{platform}_url', f'{platform}_enabled')
            ),
        }),
        ('Informacje systemowe', {
            'fields': ('created', 'updated'),
        }),
    ]
    
    def has_add_permission(self, request):
        """Only allow one instance."""
        if AboutMe.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton."""
        return False
