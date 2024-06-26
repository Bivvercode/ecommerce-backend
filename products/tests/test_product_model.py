"""
This module contains test cases for the Product model in the
products application.

Tests cover the creation and validation of products, including validation
of the product's name, description, price, discount, unit, quantity per unit,
and currency. Tests also cover the relationship between the Product and
Category models, including the ability to add, remove, and query categories
associated with a product.

Several fixtures are used to create test instances of the
Unit, Category, and Product models. These instances are used
in the test cases to create and manipulate products.

Each test case is a method on the TestProductModel class, and uses the
pytest.mark.django_db decorator to ensure that the database is
properly set up and torn down for each test.
"""
import pytest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from products.models import Product, Unit, Category


class TestProductModel:
    """Test cases for the Product model."""

    @pytest.fixture
    def unit(self):
        """Fixture for creating a unit."""
        return Unit.objects.create(name='Kilogram', symbol='kg')

    @pytest.fixture
    def category(self):
        """Fixture for creating a category."""
        return Category.objects.create(name='Electronics')

    @pytest.fixture
    def product_data(self, unit):
        """Fixture for creating product data."""
        return {
            'name': 'Test Product',
            'description': 'This is a test product',
            'price': 100.00,
            'discount': 10,
            'unit': unit,
            'quantity_per_unit': 1.00,
            'currency': 'USD'
        }

    @pytest.mark.django_db
    def test_create_product(self, product_data, category):
        """Test if a product can be created successfully."""
        product = Product.objects.create(**product_data)
        product.categories.add(category)
        assert Product.objects.count() == 1
        assert product.name == 'Test Product'
        assert product.description == 'This is a test product'
        assert product.price == 100.00
        assert product.discount == 10
        assert product.unit == product_data['unit']
        assert product.quantity_per_unit == 1.00
        assert product.currency == 'USD'
        assert product.categories.count() == 1

    @pytest.mark.django_db
    def test_product_name_cannot_be_empty(self, product_data):
        """Test if product name cannot be empty."""
        product_data['name'] = ''
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)

    @pytest.mark.django_db
    def test_product_name_cannot_exceed_200_characters(self, product_data):
        """Test if product name cannot exceed 200 characters."""
        product_data['name'] = 'a' * 201

        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['name'] = 'a' * 200
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_description_cannot_be_empty(self, product_data):
        """Test if product description cannot be empty."""
        product_data['description'] = ''
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['description'] = 'This is a test product'
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_price_cannot_be_negative(self, product_data):
        """Test if product price cannot be negative."""
        product_data['price'] = -100.00
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['price'] = 100.00
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_discount_cannot_be_negative(self, product_data):
        """Test if product discount cannot be negative."""
        product_data['discount'] = -10
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['discount'] = 10
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_discount_cannot_exceed_100(self, product_data):
        """Test if product discount cannot exceed 100."""
        product_data['discount'] = 101
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['discount'] = 100
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_unit_is_required(self, product_data):
        """Test if product unit is required."""
        product_data.pop('unit')
        with pytest.raises(ObjectDoesNotExist):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['unit'] = Unit.objects.create(name='Kilogram',
                                                   symbol='kg')
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_quantity_per_unit_cannot_be_negative(self, product_data):
        """Test if product quantity per unit cannot be negative."""
        product_data['quantity_per_unit'] = -1.00
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['quantity_per_unit'] = 1.00
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_currency_cannot_be_empty(self, product_data):
        """Test if product currency cannot be empty."""
        product_data['currency'] = ''
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['currency'] = 'USD'
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_currency_cannot_exceed_3_characters(self, product_data):
        """Test if product currency cannot exceed 3 characters."""
        product_data['currency'] = 'USDD'
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['currency'] = 'USD'
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_categories_are_optional(self, product_data):
        """Test if product categories are optional."""
        product = Product.objects.create(**product_data)
        assert product.categories.count() == 0
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_categories_are_saved(self, product_data, category):
        """Test if product categories are saved."""
        product = Product.objects.create(**product_data)
        product.categories.add(category)
        assert product.categories.count() == 1
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_categories_are_unique(self, product_data, category):
        """Test if product categories are unique."""
        product = Product.objects.create(**product_data)
        product.categories.add(category)
        product.categories.add(category)
        assert product.categories.count() == 1
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_categories_are_removed(self, product_data, category):
        """Test if product categories can be removed."""
        product = Product.objects.create(**product_data)
        product.categories.add(category)
        assert product.categories.count() == 1
        product.categories.remove(category)
        assert product.categories.count() == 0
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_in_multiple_categories(self, product_data, category):
        """Test if a product can be in multiple categories."""
        product = Product.objects.create(**product_data)
        category2 = Category.objects.create(name='Clothing')
        product.categories.add(category, category2)
        assert product.categories.count() == 2
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_str_representation(self, product_data, category):
        """Test the string representation of a product."""
        product = Product.objects.create(**product_data)
        product.categories.add(category)
        assert str(product) == 'Test Product'
