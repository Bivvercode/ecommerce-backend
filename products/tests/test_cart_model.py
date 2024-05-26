
from datetime import datetime
import pytest
from products.models import Cart
from users.models import CustomerUser


class TestCartModel:
    '''Test cases for the Cart model.'''

    @pytest.fixture
    def user(self):
        return CustomerUser.objects.create_user(
            username='testuser',
            password='12345',
            email='test@email.com',
            first_name='Test',
            last_name='User'
        )

    @pytest.mark.django_db
    def test_create_cart(self, user):
        cart = Cart.objects.create(user=user)
        assert Cart.objects.count() == 1
        assert cart.user == user
        assert isinstance(cart.created_at, datetime)

    @pytest.mark.django_db
    def test_delete_cart(self, user):
        cart = Cart.objects.create(user=user)
        assert Cart.objects.count() == 1
        cart.delete()
        assert Cart.objects.count() == 0

    @pytest.mark.django_db
    def test_user_delete_cascades(self, user):
        Cart.objects.create(user=user)
        assert Cart.objects.count() == 1
        user.delete()
        assert Cart.objects.count() == 0
