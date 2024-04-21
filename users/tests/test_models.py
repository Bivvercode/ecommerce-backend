import pytest
from users.models import CustomerUser
from django.core.exceptions import ValidationError


class TestCustomerUserModel():
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
