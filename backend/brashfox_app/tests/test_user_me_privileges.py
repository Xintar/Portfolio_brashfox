import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_me_reports_superuser_status():
    admin = User.objects.create_superuser(username='admin', password='pass12345')
    staff = User.objects.create_user(username='staff', password='pass12345', is_staff=True)
    regular = User.objects.create_user(username='regular', password='pass12345')
    client = APIClient()

    for user, expected in ((admin, True), (staff, False), (regular, False)):
        client.force_authenticate(user=user)
        assert client.get('/api/users/me/').data['is_superuser'] is expected


@pytest.mark.django_db
def test_user_list_does_not_expose_privilege_flags():
    admin = User.objects.create_superuser(username='admin', password='pass12345')
    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.get('/api/users/')
    results = response.data['results'] if isinstance(response.data, dict) else response.data

    assert all('is_superuser' not in user and 'is_staff' not in user for user in results)
