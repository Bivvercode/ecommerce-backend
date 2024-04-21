import pytest
from users.models import CustomerUser


class TestCustomerUserModel():
    @pytest.mark.django_db
    def test_custom_user_str_representation(self):
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
