import pytest
from django.core.exceptions import ValidationError
from products.models import Product, Unit, Category


class TestProductModel:
    """Test cases for the Product model."""

    @pytest.fixture
    def setup_data(self):
        unit = Unit.objects.create(name='Kilogram', symbol='kg')
        category = Category.objects.create(name='Electronics')
        return unit, category

    @pytest.mark.django_db
    def test_create_product(self, setup_data):
        unit, category = setup_data
        product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            price=100.00,
            discount=10,
            unit=unit,
            quantity_per_unit=1.00,
            currency='USD'
        )
        product.categories.add(category)
        assert Product.objects.count() == 1
        assert product.name == 'Test Product'
        assert product.description == 'This is a test product'
        assert product.price == 100.00
        assert product.discount == 10
        assert product.unit == unit
        assert product.quantity_per_unit == 1.00
        assert product.currency == 'USD'
        assert product.categories.count() == 1

    @pytest.mark.django_db
    def test_product_name_cannot_be_empty(self, setup_data):
        unit, _ = setup_data
        with pytest.raises(ValidationError):
            Product.objects.create(
                name='',
                description='This is a test product',
                price=100.00,
                discount=10,
                unit=unit,
                quantity_per_unit=1.00,
                currency='USD'
            )

    @pytest.mark.django_db
    def test_product_name_cannot_exceed_200_characters(self, setup_data):
        unit, _ = setup_data
        with pytest.raises(ValidationError):
            Product.objects.create(
                name='a' * 201,
                description='This is a test product',
                price=100.00,
                discount=10,
                unit=unit,
                quantity_per_unit=1.00,
                currency='USD'
            )

        assert Product.objects.count() == 0

        Product.objects.create(
            name='a' * 200,
            description='This is a test product',
            price=100.00,
            discount=10,
            unit=unit,
            quantity_per_unit=1.00,
            currency='USD'
        )

        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_description_cannot_be_empty(self, setup_data):
        unit, _ = setup_data
        with pytest.raises(ValidationError):
            Product.objects.create(
                name='Test Product',
                description='',
                price=100.00,
                discount=10,
                unit=unit,
                quantity_per_unit=1.00,
                currency='USD'
            )

    @pytest.mark.django_db
    def test_product_price_cannot_be_negative(self, setup_data):
        unit, _ = setup_data
        with pytest.raises(ValidationError):
            Product.objects.create(
                name='Test Product',
                description='This is a test product',
                price=-100.00,
                discount=10,
                unit=unit,
                quantity_per_unit=1.00,
                currency='USD'
            )
