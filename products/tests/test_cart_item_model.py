import pytest
from products.models import (Cart, CartItem, Product,
                             ProductCategory, Unit, Category)
from users.models import CustomerUser


class TestCartItemModel:
    '''Test cases for the CartItem model.'''

    @pytest.fixture
    def user(self):
        return CustomerUser.objects.create_user(
            username='testuser',
            password='12345',
            email='test@email.com',
            first_name='Test',
            last_name='User'
        )

    @pytest.fixture
    def unit(self):
        return Unit.objects.create(name='Test Unit', symbol='TU')

    @pytest.fixture
    def category(self):
        return Category.objects.create(name='Test Category')

    @pytest.fixture
    def cart(self, user):
        return Cart.objects.create(user=user)

    @pytest.fixture
    def product(self, unit, category):
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
        with pytest.raises(ValueError):
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=-1
            )
        assert CartItem.objects.count() == 0
