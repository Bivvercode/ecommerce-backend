import pytest
from products.models import Product, Wishlist, Unit, Category, ProductCategory
from users.models import CustomerUser


class TestWishlistModel:
    '''Test cases for the Wishlist model.'''

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
    def test_create_wishlist(self, user, product):
        wishlist = Wishlist.objects.create(user=user)
        wishlist.products.add(product)

        assert Wishlist.objects.count() == 1
        assert wishlist.user == user
        assert product in wishlist.products.all()

    @pytest.mark.django_db
    def test_remove_product_from_wishlist(self, user, product):
        wishlist = Wishlist.objects.create(user=user)
        wishlist.products.add(product)

        wishlist.products.remove(product)

        assert product not in wishlist.products.all()

    @pytest.mark.django_db
    def test_add_multiple_products_to_wishlist(self, user, product, category):
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
        wishlist.products.add(product, product2)

        assert product in wishlist.products.all()
        assert product2 in wishlist.products.all()

    @pytest.mark.django_db
    def test_add_same_product_to_multiple_wishlist(self, user, product):
        wishlist1 = Wishlist.objects.create(user=user)
        wishlist2 = Wishlist.objects.create(user=user)

        wishlist1.products.add(product)
        wishlist2.products.add(product)

        assert product in wishlist1.products.all()
        assert product in wishlist2.products.all()
