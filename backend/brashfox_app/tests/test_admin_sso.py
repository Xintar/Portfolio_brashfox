import pytest
from django.contrib.auth.models import User
from django.core import signing
from django.test import Client
from rest_framework.test import APIClient

from brashfox_app.api import admin_sso


@pytest.fixture
def staff():
    return User.objects.create_superuser(username='staff', password='pass12345')


def get_ticket(user):
    api = APIClient()
    api.force_authenticate(user=user)
    return api.post('/api/admin-sso/')


@pytest.mark.django_db
def test_ticket_requires_authentication():
    assert APIClient().post('/api/admin-sso/').status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize('flags', [{}, {'is_staff': True}])
def test_ticket_denied_for_non_superuser(flags):
    user = User.objects.create_user(username='regular', password='pass12345', **flags)
    assert get_ticket(user).status_code == 403


@pytest.mark.django_db
def test_ticket_logs_staff_into_admin(staff):
    ticket = get_ticket(staff).data['ticket']
    client = Client()

    response = client.post('/admin-sso/', {'ticket': ticket})

    assert response.status_code == 303
    assert response['Location'] == '/admin/'
    assert client.get('/admin/').status_code == 200


@pytest.mark.django_db
def test_ticket_is_single_use(staff):
    ticket = get_ticket(staff).data['ticket']

    assert Client().post('/admin-sso/', {'ticket': ticket})['Location'] == '/admin/'

    replay_client = Client()
    response = replay_client.post('/admin-sso/', {'ticket': ticket})
    assert response['Location'] == '/admin/login/'
    assert replay_client.get('/admin/').status_code == 302


@pytest.mark.django_db
def test_invalid_ticket_is_rejected():
    client = Client()
    response = client.post('/admin-sso/', {'ticket': 'garbage'})

    assert response['Location'] == '/admin/login/'
    assert client.get('/admin/').status_code == 302


@pytest.mark.django_db
def test_expired_ticket_is_rejected(staff, monkeypatch):
    ticket = get_ticket(staff).data['ticket']
    monkeypatch.setattr(admin_sso, 'TICKET_MAX_AGE', -1)

    assert Client().post('/admin-sso/', {'ticket': ticket})['Location'] == '/admin/login/'


@pytest.mark.django_db
def test_ticket_rejected_after_loss_of_superuser_status(staff):
    ticket = get_ticket(staff).data['ticket']
    staff.is_superuser = False
    staff.save()

    assert Client().post('/admin-sso/', {'ticket': ticket})['Location'] == '/admin/login/'


@pytest.mark.django_db
def test_ticket_signed_with_other_salt_is_rejected(staff):
    forged = signing.dumps({'uid': staff.pk, 'stamp': 0}, salt='other')

    assert Client().post('/admin-sso/', {'ticket': forged})['Location'] == '/admin/login/'


@pytest.mark.django_db
def test_get_is_not_allowed():
    assert Client().get('/admin-sso/').status_code == 405
