# pylint: disable=attribute-defined-outside-init
import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestChangePasswordView:
    """Test cases for the ChangePassword view."""

    @pytest.fixture
    def create_user(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Old_password1',
            email='test@gmail.com',
            first_name='Test',
            last_name='User'
        )

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_success(self):
        """Test changing the password successfully."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        data = {
            'old_password': 'Old_password1',
            'new_password': 'New_password1'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 200
        self.user.refresh_from_db()
        assert self.user.check_password('New_password1')

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_failure(self):
        """Test changing the password with wrong old password."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        data = {
            'old_password': 'wrong_password',
            'new_password': 'New_password1'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        self.user.refresh_from_db()
        assert self.user.check_password('Old_password1')
