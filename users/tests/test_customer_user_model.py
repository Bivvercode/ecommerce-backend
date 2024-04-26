"""Unit tests for the CustomerUser model.

This module contains unit tests specifically designed to validate the behavior
of the `CustomerUser` model in the `users` app of the Django project.

The tests cover various aspects of the `CustomerUser` model, including field
validation, string representation, and required field constraints.

Classes:
    TestCustomerUserModel: Test cases for the `CustomerUser` model.

Usage:
    Run this module using pytest to execute the defined
    unit tests for the `CustomerUser` model.

Example:
    To run all tests in this module using pytest:

    $ pytest users/tests/test_customer_user_model.py
"""

import pytest
from django.core.exceptions import ValidationError
from users.models import CustomerUser


class TestCustomerUserModel():
    """Test cases for the CustomerUser model."""

    @pytest.mark.django_db
    def test_customer_user_str_representation(self):
        """Test the string representation (__str__ method) of CustomUser."""
        # Create a CustomUser instance with example data
        user = CustomerUser.objects.create(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='Password123'
        )

        # Assert that the string representation matches the expected format
        expected_str = f'{user.username}'
        assert str(user) == expected_str

    @pytest.mark.django_db
    def test_customer_user_missing_username(self):
        """Test that CustomerUser requires username."""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='Password123'
            )

    @pytest.mark.django_db
    def test_customer_user_missing_email(self):
        """Test that CustomerUser requires email."""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='testuser',
                first_name='Test',
                last_name='User',
                password='Password123'
            )

    @pytest.mark.django_db
    def test_customer_user_missing_password(self):
        """Test that CustomerUser requires password."""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='testuser',
                email='test@example.com',
                first_name='Test',
                last_name='User'
            )

    @pytest.mark.django_db
    def test_customer_user_missing_first_name(self):
        """Test that CustomerUser requires first name."""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='testuser',
                email='test@example.com',
                last_name='User',
                password='Password123'
            )

    @pytest.mark.django_db
    def test_customer_user_missing_last_name(self):
        """Test that CustomerUser requires last name."""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='testuser',
                email='test@example.com',
                first_name='Test',
                password='Password123'
            )

    @pytest.mark.django_db
    def test_customer_user_invalid_email(self):
        """Test that CustomerUser requires a valid email."""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='testuser',
                email='test.example.com',
                first_name='Test',
                last_name='User',
                password='Password123'
            )

    @pytest.mark.django_db
    def test_customer_user_username_max_length(self):
        """Test that CustomerUser is not allowing username over max length"""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='Twenty-1_characters.0',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='Password123'
            )

    @pytest.mark.django_db
    def test_customer_user_username_min_length(self):
        """Test that CustomerUser is not allowing username under min length"""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='cat',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='Password123'
            )

    @pytest.mark.django_db
    def test_customer_user_password_min_length(self):
        """Test that CustomerUser is not allowing password under min length"""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='TestUser',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='Short@1'
            )

    @pytest.mark.django_db
    def test_customer_user_phone_number_max_length(self):
        """
        Test that CustomerUser is not allowing phone number over max length
        """
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='TestUser',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                phone_number='+46700112233445566721',
                password='Password123'
            )

    @pytest.mark.django_db
    def test_uniqueness_username(self):
        """Test that CustomerUser username is unique"""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='Duplicate',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='Password123'
            )
            CustomerUser.objects.create(
                username='Duplicate',
                email='test2@example.com',
                first_name='Test',
                last_name='User',
                password='Password123'
            )

    @pytest.mark.django_db
    def test_uniqueness_email(self):
        """Test that CustomerUser email is unique"""
        with pytest.raises(ValidationError):
            CustomerUser.objects.create(
                username='Testuser',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='Password123'
            )
            CustomerUser.objects.create(
                username='Testuser123',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='Password123'
            )
