import pytest

from brashfox_app.models import BlogPost


@pytest.mark.django_db
def test_blog_post_list(client):
    post = BlogPost
    response = client
    assert response