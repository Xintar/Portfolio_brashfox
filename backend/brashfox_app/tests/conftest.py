import pytest
from django.test import Client

from brashfox_app.models import BlogPost


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def post():
    pass
    # post =