"""
This module contains test cases for the ProductCategory model
in the products app.

Tests cover the creation and deletion of product categories, validation
of the product and category fields, and the cascading deletion of
product categories when their associated product or category is deleted.

Several fixtures are used to create test instances of the Unit,
Category, and Product models. These instances are used in the
test cases to create and manipulate product categories.

Each test case is a method on the TestProductCategoryModel class,
and uses the pytest.mark.django_db decorator to ensure that
the database is properly set up and torn down for each test.
"""

import pytest
from django.db import IntegrityError, transaction
from products.models import ProductCategory, Category, Product, Unit


class TestProductCategoryModel:
    """Test cases for the ProductCategory model."""

    @pytest.fixture
    def unit(self):
        """Fixture for creating a test unit."""
        return Unit.objects.create(name='Kilogram', symbol='kg')

    @pytest.fixture
    def category(self):
        """Fixture for creating a test category."""
        return Category.objects.create(name='Electronics')

    @pytest.fixture
    def product(self, unit):
        """Fixture for creating a test product with a unit."""
        return Product.objects.create(
            name='Test Product',
            description='This is a test product',
            price=100.00,
            discount=10,
            unit=unit,
            quantity_per_unit=1.00,
            currency='USD'
        )

    @pytest.mark.django_db
    def test_create_product_category(self, product, category):
        """
        Test that a product category can be created with a
        product and a category.
        """
        product_category = ProductCategory.objects.create(product=product,
                                                          category=category)
        assert ProductCategory.objects.count() == 1
        assert product_category.product == product
        assert product_category.category == category

    @pytest.mark.django_db
    def test_product_category_product_is_required(self, category):
        """Test that a product category cannot be created without a product."""
        with pytest.raises(IntegrityError):
            with transaction.atomic():
                ProductCategory.objects.create(category=category)
        assert ProductCategory.objects.count() == 0

    @pytest.mark.django_db
    def test_product_category_category_is_required(self, product):
        """
        Test that a product category cannot be created without a category.
        """
        with pytest.raises(IntegrityError):
            with transaction.atomic():
                ProductCategory.objects.create(product=product)
        assert ProductCategory.objects.count() == 0

    @pytest.mark.django_db
    def test_product_delete_cascades(self, product, category):
        """
        Test that deleting a product also deletes its associated
        product categories.
        """
        ProductCategory.objects.create(product=product, category=category)
        assert ProductCategory.objects.count() == 1
        product.delete()
        assert ProductCategory.objects.count() == 0

    @pytest.mark.django_db
    def test_category_delete_cascades(self, product, category):
        """
        Test that deleting a category also deletes its associated
        product categories.
        """
        ProductCategory.objects.create(product=product, category=category)
        assert ProductCategory.objects.count() == 1
        category.delete()
        assert ProductCategory.objects.count() == 0

    @pytest.mark.django_db
    def test_multiple_categories_for_product(self, product, category):
        """Test that a product can have multiple categories."""
        ProductCategory.objects.create(product=product, category=category)
        assert ProductCategory.objects.count() == 1
        category2 = Category.objects.create(name='Clothing')
        ProductCategory.objects.create(product=product, category=category2)
        assert ProductCategory.objects.count() == 2
        category3 = Category.objects.create(name='Footwear')
        ProductCategory.objects.create(product=product, category=category3)
        assert ProductCategory.objects.count() == 3
        assert product.categories.count() == 3

    @pytest.mark.django_db
    def test_multiple_products_for_category(self, product, category):
        """Test that a category can have multiple products."""
        ProductCategory.objects.create(product=product, category=category)
        assert ProductCategory.objects.count() == 1
        product2 = Product.objects.create(
            name='Test Product 2',
            description='This is a test product',
            price=100.00,
            discount=10,
            unit=product.unit,
            quantity_per_unit=1.00,
            currency='USD'
        )
        ProductCategory.objects.create(product=product2, category=category)
        assert ProductCategory.objects.count() == 2
        product3 = Product.objects.create(
            name='Test Product 3',
            description='This is a test product',
            price=100.00,
            discount=10,
            unit=product.unit,
            quantity_per_unit=1.00,
            currency='USD'
        )
        ProductCategory.objects.create(product=product3, category=category)
        assert ProductCategory.objects.count() == 3
