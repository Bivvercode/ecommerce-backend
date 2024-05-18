# pylint: disable=attribute-defined-outside-init
import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestProfileView:
    """Test cases for the Profile view."""

    @pytest.fixture
    def create_user(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpass123!',
            email='test@gmail.com',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            shipping_address='Test Shipping Address',
            billing_address='Test Billing Address'
        )

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_get_profile(self):
        """Test getting the profile."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('profile')
        response = client.get(url)
        assert response.status_code == 200
        assert response.data['username'] == 'testuser'
        assert response.data['first_name'] == 'Test'
        assert response.data['last_name'] == 'User'
        assert response.data['email'] == 'test@gmail.com'
        assert response.data['phone_number'] == '1234567890'
        assert response.data['shipping_address'] == 'Test Shipping Address'
        assert response.data['billing_address'] == 'Test Billing Address'

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_get_profile_without_token(self):
        """Test getting the profile without token."""
        client = APIClient()
        url = reverse('profile')
        response = client.get(url)
        assert response.status_code == 401

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_update_profile(self):
        """Test updating the profile."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('profile')
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@gmail.com',
            'phone_number': '0987654321',
            'shipping_address': 'Updated Shipping Address',
            'billing_address': 'Updated Billing Address'
        }
        response = client.put(url, data, format='json')
        assert response.status_code == 200
        self.user.refresh_from_db()
        assert self.user.first_name == 'Updated'
        assert self.user.last_name == 'User'
        assert self.user.email == 'updated@gmail.com'
        assert self.user.phone_number == '0987654321'
        assert self.user.shipping_address == 'Updated Shipping Address'
        assert self.user.billing_address == 'Updated Billing Address'

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_update_profile_without_token(self):
        """Test updating the profile without token."""
        client = APIClient()
        url = reverse('profile')
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@gmail.com',
            'phone_number': '0987654321',
            'shipping_address': 'Updated Shipping Address',
            'billing_address': 'Updated Billing Address'
        }
        response = client.put(url, data, format='json')
        assert response.status_code == 401
