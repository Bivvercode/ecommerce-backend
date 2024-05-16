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
