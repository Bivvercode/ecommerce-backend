"""
Tests for the Password views.

This module contains test cases for the password views in the application.
It tests the functionality of changing a user's password.

Each class in this module tests a specific view, and each method
tests a specific functionality or edge case.

Classes:
    TestChangePasswordView: Test cases for the ChangePassword view.
"""
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

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_without_token(self):
        """Test changing the password without token."""
        client = APIClient()
        url = reverse('change_password')
        data = {
            'old_password': 'Old_password1',
            'new_password': 'New_password1'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 401

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_without_old_password(self):
        """Test changing the password without old password."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        data = {'new_password': 'New_password1'}
        response = client.post(url, data, format='json')
        assert response.status_code == 400

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_without_new_password(self):
        """Test changing the password without new password."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        data = {'old_password': 'Old_password1'}
        response = client.post(url, data, format='json')
        assert response.status_code == 400

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_without_old_and_new_password(self):
        """Test changing the password without old and new password."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        response = client.post(url)
        assert response.status_code == 400

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_without_number(self):
        """Test changing the password with a password missing a number."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        data = {
            'old_password': 'Old_password1',
            'new_password': 'New_password'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        self.user.refresh_from_db()
        assert self.user.check_password('Old_password1')

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_without_uppercase(self):
        """
        Test changing the password with a password missing an uppercase letter.
        """
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        data = {
            'old_password': 'Old_password1',
            'new_password': 'new_password1'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        self.user.refresh_from_db()
        assert self.user.check_password('Old_password1')

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_without_lowercase(self):
        """
        Test changing the password with a password missing a lowercase letter.
        """
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        data = {
            'old_password': 'Old_password1',
            'new_password': 'NEW_PASSWORD1'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        self.user.refresh_from_db()
        assert self.user.check_password('Old_password1')

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_without_special_character(self):
        """
        Test changing the password with a password missing a special character.
        """
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        data = {
            'old_password': 'Old_password1',
            'new_password': 'Newpassword1'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        self.user.refresh_from_db()
        assert self.user.check_password('Old_password1')

    @pytest.mark.usefixtures('create_user')
    @pytest.mark.django_db
    def test_change_password_with_short_password(self):
        """Test changing the password with a password that is too short."""
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('change_password')
        data = {
            'old_password': 'Old_password1',
            'new_password': 'Short_1'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        self.user.refresh_from_db()
        assert self.user.check_password('Old_password1')
