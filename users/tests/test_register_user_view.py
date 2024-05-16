import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomerUser


class TestRegisterView:
    """Test cases for the RegisterView view."""

    @pytest.mark.django_db
    def test_register_user(self):
        """Test registering a new user."""
        client = APIClient()
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'Testpassword1!',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 201
        assert 'token' in response.data
        assert CustomerUser.objects.filter(username='testuser').exists()

    @pytest.mark.django_db
    def test_register_user_no_password(self):
        """Test registering a new user without a password."""
        client = APIClient()
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        assert 'password' in response.data
        assert not CustomerUser.objects.filter(username='testuser').exists()

    @pytest.mark.django_db
    def test_register_user_no_username(self):
        """Test registering a new user without a username."""
        client = APIClient()
        url = reverse('register')
        data = {
            'password': 'StrongPassword123!',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        assert 'username' in response.data
        assert not CustomerUser.objects.filter(email='test@email.com').exists()

    @pytest.mark.django_db
    def test_register_user_no_email(self):
        """Test registering a new user without an email."""
        client = APIClient()
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'StrongPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        assert 'email' in response.data
        assert not CustomerUser.objects.filter(username='testuser').exists()

    @pytest.mark.django_db
    def test_register_user_no_first_name(self):
        """Test registering a new user without a first name."""
        client = APIClient()
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'StrongPassword123!',
            'email': 'test@email.com',
            'last_name': 'User'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        assert 'first_name' in response.data
        assert not CustomerUser.objects.filter(username='testuser').exists()
