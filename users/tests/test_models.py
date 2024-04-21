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
            last_name='User'
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
                last_name='User'
            )
