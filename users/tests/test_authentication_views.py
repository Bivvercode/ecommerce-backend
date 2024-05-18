# pylint: disable=attribute-defined-outside-init
import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestAuthenticationView:
    """Test cases for the Authentication views."""
    @pytest.fixture
    def create_user(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123!',
            email='test@gmail.com',
            first_name='Test',
            last_name='User'
        )

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_login_with_valid_credentials(self):
        """Test logging in with valid credentials."""
        client = APIClient()
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass123!'}
        response = client.post(url, data, format='json')
        assert response.status_code == 200
        assert 'token' in response.data

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_login_with_invalid_credentials(self):
        """Test logging in with invalid credentials."""
        client = APIClient()
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = client.post(url, data, format='json')
        assert response.status_code == 400

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_login_without_credentials(self):
        """Test logging in without credentials."""
        client = APIClient()
        url = reverse('login')
        response = client.post(url)
        assert response.status_code == 400

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_login_without_username(self):
        """Test logging in without username."""
        client = APIClient()
        url = reverse('login')
        data = {'password': 'testpass123!'}
        response = client.post(url, data, format='json')
        assert response.status_code == 400

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_login_without_password(self):
        """Test logging in without password."""
        client = APIClient()
        url = reverse('login')
        data = {'username': 'testuser'}
        response = client.post(url, data, format='json')
        assert response.status_code == 400

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_login_with_nonexistent_user(self):
        """Test logging in with a nonexistent user."""
        client = APIClient()
        url = reverse('login')
        data = {'username': 'nonexistent', 'password': 'testpass123!'}
        response = client.post(url, data, format='json')
        assert response.status_code == 400

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_logout(self):
        """Test logging out."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('logout')
        response = client.post(url)
        assert response.status_code == 200

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_logout_without_token(self):
        """Test logging out without token."""
        client = APIClient()
        url = reverse('logout')
        response = client.post(url)
        assert response.status_code == 401

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_logout_with_invalid_token(self):
        """Test logging out with invalid token."""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        url = reverse('logout')
        response = client.post(url)
        assert response.status_code == 401
