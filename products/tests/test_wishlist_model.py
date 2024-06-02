"""
This module contains test cases for the Wishlist model in
the products application.

Tests cover the creation and manipulation of wishlists, including
adding and removing products, and handling of non-existent products and users.

Each test case is a method on the TestWishlistModel class, and uses
the pytest.mark.django_db decorator to ensure that the database
is properly set up and torn down for each test.
"""

import pytest
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product, Wishlist, Unit, Category, ProductCategory
from users.models import CustomerUser


class TestWishlistModel:
    """Test cases for the Wishlist model."""

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
    def product(self, unit, category):
        """Fixture for creating a test product."""
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
    def test_create_wishlist(self, user, product):
        """Test the creation of a wishlist and adding a product to it."""
        wishlist = Wishlist.objects.create(user=user)
        wishlist.add_product(product)

        assert Wishlist.objects.count() == 1
        assert wishlist.user == user
        assert product in wishlist.products.all()

    @pytest.mark.django_db
    def test_remove_product_from_wishlist(self, user, product):
        """Test the removal of a product from a wishlist."""
        wishlist = Wishlist.objects.create(user=user)
        wishlist.add_product(product)

        wishlist.products.remove(product)

        assert product not in wishlist.products.all()

    @pytest.mark.django_db
    def test_add_multiple_products_to_wishlist(self, user, product, category):
        """Test the addition of multiple products to a wishlist."""
        product2 = Product.objects.create(
            name='Test Product 2',
            description='This is a test product',
            price=100.00,
            discount=10,
            unit=product.unit,
            quantity_per_unit=1.00,
            currency='USD'
        )
        ProductCategory.objects.create(product=product2,
                                       category=category)

        wishlist = Wishlist.objects.create(user=user)
        wishlist.add_product(product)
        wishlist.add_product(product2)

        assert product in wishlist.products.all()
        assert product2 in wishlist.products.all()

    @pytest.mark.django_db
    def test_add_same_product_to_multiple_wishlist(self, user, product):
        """Test the addition of the same product to multiple wishlists."""
        wishlist1 = Wishlist.objects.create(user=user)
        wishlist2 = Wishlist.objects.create(user=user)

        wishlist1.add_product(product)
        wishlist2.add_product(product)

        assert product in wishlist1.products.all()
        assert product in wishlist2.products.all()

    @pytest.mark.django_db
    def test_create_wishlist_without_user(self):
        """Test the creation of a wishlist without a user."""
        with pytest.raises(ObjectDoesNotExist):
            Wishlist.objects.create()
        assert Wishlist.objects.count() == 0

    @pytest.mark.django_db
    def test_add_nonexistent_product_to_wishlist(self, user):
        """Test the addition of a non-existent product to a wishlist."""
        wishlist = Wishlist.objects.create(user=user)
        with pytest.raises(ValueError):
            wishlist.add_product(None)
