import pytest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from products.models import Product, Unit, Category


class TestProductModel:
    """Test cases for the Product model."""

    @pytest.fixture
    def unit(self):
        return Unit.objects.create(name='Kilogram', symbol='kg')

    @pytest.fixture
    def category(self):
        return Category.objects.create(name='Electronics')

    @pytest.fixture
    def product_data(self, unit):
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
        product_data['name'] = ''
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)

    @pytest.mark.django_db
    def test_product_name_cannot_exceed_200_characters(self, product_data):
        product_data['name'] = 'a' * 201

        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['name'] = 'a' * 200
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_description_cannot_be_empty(self, product_data):
        product_data['description'] = ''
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['description'] = 'This is a test product'
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_price_cannot_be_negative(self, product_data):
        product_data['price'] = -100.00
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['price'] = 100.00
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_discount_cannot_be_negative(self, product_data):
        product_data['discount'] = -10
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['discount'] = 10
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_discount_cannot_exceed_100(self, product_data):
        product_data['discount'] = 101
        with pytest.raises(ValidationError):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['discount'] = 100
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_unit_is_required(self, product_data):
        product_data.pop('unit')
        with pytest.raises(ObjectDoesNotExist):
            Product.objects.create(**product_data)
        assert Product.objects.count() == 0

        product_data['unit'] = Unit.objects.create(name='Kilogram',
                                                   symbol='kg')
        Product.objects.create(**product_data)
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_quantity_per_unit_cannot_be_negative(self, setup_data):
        unit, _ = setup_data
        with pytest.raises(ValidationError):
            Product.objects.create(
                name='Test Product',
                description='This is a test product',
                price=100.00,
                discount=10,
                unit=unit,
                quantity_per_unit=-1.00,
                currency='USD'
            )

    @pytest.mark.django_db
    def test_product_currency_cannot_be_empty(self, setup_data):
        unit, _ = setup_data
        with pytest.raises(ValidationError):
            Product.objects.create(
                name='Test Product',
                description='This is a test product',
                price=100.00,
                discount=10,
                unit=unit,
                quantity_per_unit=1.00,
                currency=''
            )

    @pytest.mark.django_db
    def test_product_currency_cannot_exceed_3_characters(self, setup_data):
        unit, _ = setup_data
        with pytest.raises(ValidationError):
            Product.objects.create(
                name='Test Product',
                description='This is a test product',
                price=100.00,
                discount=10,
                unit=unit,
                quantity_per_unit=1.00,
                currency='USDD'
            )

    @pytest.mark.django_db
    def test_product_categories_are_optional(self, setup_data):
        unit, _ = setup_data
        product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            price=100.00,
            discount=10,
            unit=unit,
            quantity_per_unit=1.00,
            currency='USD'
        )
        assert product.categories.count() == 0
        assert Product.objects.count() == 1

    @pytest.mark.django_db
    def test_product_categories_are_saved(self, setup_data):
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
        assert product.categories.count() == 1
        assert Product.objects.count() == 1
