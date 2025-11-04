import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from brashfox_app.models import BlogPost, FotoDescription, Message


@pytest.mark.django_db
class TestBlogPostPermissions:
    """Test permissions for BlogPost endpoints"""
    
    def setup_method(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='admin123')
        
        self.post1 = BlogPost.objects.create(
            title='User1 Post',
            post='Content by user1',
            slug='user1-post',  # Set slug explicitly
            author=self.user1
        )
    
    def test_list_posts_anonymous(self):
        """Anonymous users can list posts"""
        response = self.client.get('/api/blog-posts/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_retrieve_post_anonymous(self):
        """Anonymous users can view post details"""
        response = self.client.get(f'/api/blog-posts/{self.post1.slug}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'User1 Post'
    
    def test_create_post_anonymous(self):
        """Anonymous users cannot create posts"""
        response = self.client.post('/api/blog-posts/', {
            'title': 'New Post',
            'post': 'Content'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_post_authenticated(self):
        """Authenticated users can create posts"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/blog-posts/', {
            'title': 'New Post',
            'post': 'Content'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['author']['username'] == 'user1'
    
    def test_update_own_post(self):
        """Users can update their own posts"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f'/api/blog-posts/{self.post1.slug}/', {
            'title': 'Updated Title'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
    
    def test_update_other_user_post(self):
        """Users cannot update other users' posts"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(f'/api/blog-posts/{self.post1.slug}/', {
            'title': 'Hacked Title'
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_post_as_admin(self):
        """Admins can update any post"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(f'/api/blog-posts/{self.post1.slug}/', {
            'title': 'Admin Updated'
        })
        assert response.status_code == status.HTTP_200_OK
    
    def test_delete_own_post(self):
        """Users can delete their own posts"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/blog-posts/{self.post1.slug}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_delete_other_user_post(self):
        """Users cannot delete other users' posts"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f'/api/blog-posts/{self.post1.slug}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestAutoSlugGeneration:
    """Test automatic slug generation"""
    
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.force_authenticate(user=self.user)
    
    def test_slug_generated_from_title(self):
        """Slug is automatically generated from title"""
        response = self.client.post('/api/blog-posts/', {
            'title': 'My First Post',
            'post': 'Content'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['slug'] == 'my-first-post'
    
    def test_slug_unique_incremental(self):
        """Duplicate titles get incremental slugs"""
        # First post
        response1 = self.client.post('/api/blog-posts/', {
            'title': 'Duplicate Title',
            'post': 'Content 1'
        })
        assert response1.data['slug'] == 'duplicate-title'
        
        # Second post with same title
        response2 = self.client.post('/api/blog-posts/', {
            'title': 'Duplicate Title',
            'post': 'Content 2'
        })
        assert response2.data['slug'] == 'duplicate-title-1'


@pytest.mark.django_db
class TestMessageThrottling:
    """Test rate limiting for contact form"""
    
    def setup_method(self):
        self.client = APIClient()
    
    def test_message_creation_allowed(self):
        """Anonymous users can send messages (within limit)"""
        response = self.client.post('/api/messages/', {
            'name': 'John Doe',
            'email': 'john@test.com',
            'topic': 'Question',
            'message': 'Test message'
        })
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_message_list_requires_auth(self):
        """Only authenticated users can list messages"""
        response = self.client.get('/api/messages/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration"""
    
    def setup_method(self):
        self.client = APIClient()
    
    def test_register_new_user(self):
        """Users can register with valid data"""
        response = self.client.post('/api/users/', {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'SecurePass123!'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'newuser'
        assert 'password' not in response.data
    
    def test_register_duplicate_username(self):
        """Cannot register with existing username"""
        User.objects.create_user(username='existing', password='pass123')
        
        response = self.client.post('/api/users/', {
            'username': 'existing',
            'email': 'new@test.com',
            'password': 'pass123'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPhotoPermissions:
    """Test permissions for photo endpoints"""
    
    def setup_method(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='photographer', password='pass123')
        self.user2 = User.objects.create_user(username='other', password='pass123')
    
    def test_list_photos_anonymous(self):
        """Anonymous users can view photos"""
        response = self.client.get('/api/photos/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_photo_requires_auth(self):
        """Creating photos requires authentication"""
        response = self.client.post('/api/photos/', {
            'name': 'Test Photo',
            'author': 'photographer'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_photo_authenticated(self):
        """Authenticated users can create photos"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/photos/', {
            'name': 'Test Photo',
            'event': 'Test Event'
        })
        # Author should be set automatically
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['author'] == 'photographer'


@pytest.mark.django_db
class TestJWTAuthentication:
    """Test JWT token authentication"""
    
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_obtain_token(self):
        """Users can obtain JWT tokens"""
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_obtain_token_invalid_credentials(self):
        """Invalid credentials return 401"""
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_access_protected_endpoint_with_token(self):
        """JWT token grants access to protected endpoints"""
        # Get token
        token_response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        access_token = token_response.data['access']
        
        # Use token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'


@pytest.mark.django_db
class TestSearchAndFiltering:
    """Test search and filtering functionality"""
    
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='author', password='pass123')
        
        BlogPost.objects.create(title='Django Tutorial', slug='django-tutorial', post='Learn Django', author=self.user)
        BlogPost.objects.create(title='React Guide', slug='react-guide', post='Learn React', author=self.user)
        BlogPost.objects.create(title='Python Tips', slug='python-tips', post='Python tricks', author=self.user)
    
    def test_search_blog_posts(self):
        """Search works across title and content"""
        response = self.client.get('/api/blog-posts/?search=Django')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'Django Tutorial'
    
    def test_filter_by_author(self):
        """Can filter posts by author"""
        response = self.client.get(f'/api/blog-posts/?author={self.user.id}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3
    
    def test_ordering(self):
        """Can order by created date"""
        response = self.client.get('/api/blog-posts/?ordering=-created')
        assert response.status_code == status.HTTP_200_OK
        # Newest first
        assert response.data['results'][0]['title'] == 'Python Tips'
