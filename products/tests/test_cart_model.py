"""
This module contains test cases for the Cart model in the products app.

Tests cover the creation and deletion of carts, as well as the cascading
deletion of carts when their associated user is deleted.

A fixture is used to create a test instance of the User model.
This instance is used in the test cases to create and manipulate carts.

Each test case is a method on the TestCartModel class,
and uses the pytest.mark.django_db decorator to ensure that
the database is properly set up and torn down for each test.
"""
from datetime import datetime
import pytest
from products.models import Cart
from users.models import CustomerUser


class TestCartModel:
    """Test cases for the Cart model."""

    @pytest.fixture
    def user(self):
        """Fixture for creating a test user."""
        return CustomerUser.objects.create_user(
            username='testuser',
            password='12345',
            email='test@email.com',
            first_name='Test',
            last_name='User'
        )

    @pytest.mark.django_db
    def test_create_cart(self, user):
        """Test that a cart can be created with a user."""
        cart = Cart.objects.create(user=user)
        assert Cart.objects.count() == 1
        assert cart.user == user
        assert isinstance(cart.created_at, datetime)

    @pytest.mark.django_db
    def test_delete_cart(self, user):
        """Test that a cart can be deleted."""
        cart = Cart.objects.create(user=user)
        assert Cart.objects.count() == 1
        cart.delete()
        assert Cart.objects.count() == 0

    @pytest.mark.django_db
    def test_user_delete_cascades(self, user):
        """Test that deleting a user also deletes their associated cart."""
        Cart.objects.create(user=user)
        assert Cart.objects.count() == 1
        user.delete()
        assert Cart.objects.count() == 0
