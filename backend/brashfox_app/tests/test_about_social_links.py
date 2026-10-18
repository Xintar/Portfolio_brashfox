import pytest
from django.contrib import admin
from django.test import RequestFactory
from rest_framework.test import APIClient

from brashfox_app.admin import AboutMeAdmin
from brashfox_app.models import AboutMe
from brashfox_app.models.about import SOCIAL_PLATFORM_CHOICES


def test_about_admin_exposes_every_social_platform():
    admin_form = AboutMeAdmin(AboutMe, admin.site).get_form(
        RequestFactory().get('/admin/')
    )

    for platform, _ in SOCIAL_PLATFORM_CHOICES:
        assert f'{platform}_url' in admin_form.base_fields
        assert f'{platform}_enabled' in admin_form.base_fields

    fieldset_fields = [
        field
        for _, options in AboutMeAdmin(AboutMe, admin.site).fieldsets
        for field in options['fields']
    ]
    for platform, _ in SOCIAL_PLATFORM_CHOICES:
        assert f'{platform}_url' in fieldset_fields
        assert f'{platform}_enabled' in fieldset_fields


@pytest.mark.django_db
def test_about_admin_saves_social_urls_and_visibility():
    about = AboutMe.objects.create(
        title='O mnie',
        name='Marta',
        bio='Biografia',
        profile_image='about/profile.png',
    )
    admin_form = AboutMeAdmin(AboutMe, admin.site).get_form(
        RequestFactory().get('/admin/')
    )
    form = admin_form(
        data={
            'title': 'O mnie',
            'name': 'Marta',
            'bio': 'Biografia',
            'specializations': '[]',
            'instagram_url': 'https://instagram.com/example',
            'instagram_enabled': 'on',
            'facebook_url': 'https://facebook.com/example',
        },
        instance=about,
    )

    assert form.is_valid(), form.errors
    about = form.save()

    assert about.social_links == {
        'instagram': {
            'enabled': True,
            'url': 'https://instagram.com/example',
        },
        'facebook': {
            'enabled': False,
            'url': 'https://facebook.com/example',
        },
    }
    assert about.enabled_social_links == [{
        'platform': 'instagram',
        'label': 'Instagram',
        'url': 'https://instagram.com/example',
    }]


@pytest.mark.django_db
def test_about_admin_requires_url_for_enabled_social_profile():
    about = AboutMe.objects.create(
        title='O mnie',
        name='Marta',
        bio='Biografia',
        profile_image='about/profile.png',
    )
    admin_form = AboutMeAdmin(AboutMe, admin.site).get_form(
        RequestFactory().get('/admin/')
    )
    form = admin_form(
        data={
            'title': 'O mnie',
            'name': 'Marta',
            'bio': 'Biografia',
            'specializations': '[]',
            'instagram_enabled': 'on',
        },
        instance=about,
    )

    assert not form.is_valid()
    assert 'instagram_url' in form.errors


@pytest.mark.django_db
def test_about_api_returns_only_enabled_social_profiles():
    AboutMe.objects.create(
        title='O mnie',
        name='Marta',
        bio='Biografia',
        profile_image='about/profile.png',
        social_links={
            'instagram': {
                'enabled': True,
                'url': 'https://instagram.com/example',
            },
            'facebook': {
                'enabled': False,
                'url': 'https://facebook.com/example',
            },
        },
    )

    response = APIClient().get('/api/about/')

    assert response.status_code == 200
    assert response.data['social_links'] == [{
        'platform': 'instagram',
        'label': 'Instagram',
        'url': 'https://instagram.com/example',
    }]
