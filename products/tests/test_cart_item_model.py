"""
This module contains test cases for the CartItem model in the products app.

Tests cover the creation and deletion of cart items, as well as the cascading
deletion of cart items when their associated cart or product is deleted.

Fixtures are used to create test instances of the User, Unit,
Category, Cart, and Product models. These instances are used in
the test cases to create and manipulate cart items.

Each test case is a method on the TestCartItemModel class, and uses
the pytest.mark.django_db decorator to ensure that the database is
properly set up and torn down for each test.
"""
import pytest
from django.core.exceptions import ObjectDoesNotExist
from products.models import (Cart, CartItem, Product,
                             ProductCategory, Unit, Category)
from users.models import CustomerUser


class TestCartItemModel:
    """Test cases for the CartItem model."""

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

    @pytest.fixture
    def unit(self):
        """Fixture for creating a test unit."""
        return Unit.objects.create(name='Test Unit', symbol='TU')

    @pytest.fixture
    def category(self):
        """Fixture for creating a test category."""
        return Category.objects.create(name='Test Category')

    @pytest.fixture
    def cart(self, user):
        """Fixture for creating a test cart associated with a test user."""
        return Cart.objects.create(user=user)

    @pytest.fixture
    def product(self, unit, category):
        """
        Fixture for creating a test product associated
        with atest unit and category.
        """
        product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            price=100.00,
            discount=10,
            unit=unit,
            quantity_per_unit=1.00,
            currency='USD'
        )
        ProductCategory.objects.create(product=product, category=category)
        return product

    @pytest.mark.django_db
    def test_create_cart_item(self, cart, product):
        """Test that a cart item can be created with a cart and a product."""
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )
        assert CartItem.objects.count() == 1
        assert cart_item.cart == cart
        assert cart_item.product == product
        assert cart_item.quantity == 1

    @pytest.mark.django_db
    def test_delete_cart_item(self, cart, product):
        """Test that a cart item can be deleted."""
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )
        assert CartItem.objects.count() == 1
        cart_item.delete()
        assert CartItem.objects.count() == 0

    @pytest.mark.django_db
    def test_cart_delete_cascades(self, cart, product):
        """Test that deleting a cart also deletes its associated cart items."""
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )
        assert CartItem.objects.count() == 1
        cart.delete()
        assert CartItem.objects.count() == 0

    @pytest.mark.django_db
    def test_product_delete_cascades(self, cart, product):
        """
        Test that deleting a product also deletes its associated cart items.
        """
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )
        assert CartItem.objects.count() == 1
        product.delete()
        assert CartItem.objects.count() == 0

    @pytest.mark.django_db
    def test_add_multiple_products_to_cart(self, cart, product):
        """Test that multiple products can be added to a cart."""
        cart_item_1 = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )
        product_2 = Product.objects.create(
            name='Test Product 2',
            description='This is a test product',
            price=100.00,
            discount=10,
            unit=product.unit,
            quantity_per_unit=1.00,
            currency='USD'
        )
        cart_item_2 = CartItem.objects.create(
            cart=cart,
            product=product_2,
            quantity=2
        )
        assert CartItem.objects.count() == 2
        assert cart_item_1.quantity == 1
        assert cart_item_2.quantity == 2

    @pytest.mark.django_db
    def test_cart_item_quantity_cannot_be_negative(self, cart, product):
        """Test that a cart item cannot be created with a negative quantity."""
        with pytest.raises(ValueError):
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=-1
            )
        assert CartItem.objects.count() == 0

    @pytest.mark.django_db
    def test_cart_item_quantity_cannot_be_zero(self, cart, product):
        """Test that a cart item cannot be created with a quantity of zero."""
        with pytest.raises(ValueError):
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=0
            )
        assert CartItem.objects.count() == 0

    @pytest.mark.django_db
    def test_cart_item_cart_cannot_be_empty(self, product):
        """Test that a cart item cannot be created without a cart."""
        with pytest.raises(ObjectDoesNotExist):
            CartItem.objects.create(
                product=product,
                quantity=1
            )
        assert CartItem.objects.count() == 0

    @pytest.mark.django_db
    def test_cart_item_product_cannot_be_empty(self, cart):
        """Test that a cart item cannot be created without a product."""
        with pytest.raises(ObjectDoesNotExist):
            CartItem.objects.create(
                cart=cart,
                quantity=1
            )
        assert CartItem.objects.count() == 0
