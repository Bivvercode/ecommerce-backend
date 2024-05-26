import os
from pathlib import Path
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from products.models import Image, Product, Unit, Category, ProductCategory


class TestImageModel:
    '''Test cases for the Image model.'''

    @pytest.fixture
    def unit(self):
        return Unit.objects.create(name='Kilogram', symbol='kg')

    @pytest.fixture
    def category(self):
        return Category.objects.create(name='Electronics')

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

    @pytest.fixture
    def image_file(self, tmp_path):
        file = tmp_path / "test_image.jpg"
        file.write_bytes(b'')
        uploaded_file = SimpleUploadedFile(name='test_image.jpg',
                                           content=Path(file).read_bytes(),
                                           content_type='image/jpeg')

        yield uploaded_file

        file_path = os.path.join(settings.MEDIA_ROOT,
                                 'product_images',
                                 uploaded_file.name)
        if os.path.exists(file_path):
            os.remove(file_path)

    @pytest.mark.django_db
    def test_create_image(self, product, image_file):
        image = Image.objects.create(image_file=image_file, product=product)
        assert Image.objects.count() == 1
        assert image.image_file.name == 'product_images/test_image.jpg'
        assert image.product == product

    @pytest.mark.django_db
    def test_delete_image(self, product, image_file):
        image = Image.objects.create(image_file=image_file, product=product)
        assert Image.objects.count() == 1
        image.delete()
        assert Image.objects.count() == 0

    @pytest.mark.django_db
    def test_product_delete_cascades(self, product, image_file):
        Image.objects.create(image_file=image_file, product=product)
        assert Image.objects.count() == 1
        product.delete()
        assert Image.objects.count() == 0

    @pytest.mark.django_db
    def test_image_file_cannot_be_empty(self, product):
        with pytest.raises(ValidationError):
            Image.objects.create(image_file=None, product=product)
        assert Image.objects.count() == 0

    @pytest.mark.django_db
    def test_product_cannot_be_empty(self, image_file):
        with pytest.raises(ObjectDoesNotExist):
            Image.objects.create(image_file=image_file, product=None)
        assert Image.objects.count() == 0

    @pytest.mark.django_db
    def test_image_str(self, product, image_file):
        image = Image.objects.create(image_file=image_file, product=product)
        assert str(image) == f'{product.name} Image'
