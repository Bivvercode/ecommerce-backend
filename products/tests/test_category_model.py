import pytest
from django.core.exceptions import ValidationError
from products.models import Category


class TestCategoryModel:
    """Test cases for the Category model."""

    @pytest.mark.django_db
    def test_create_category(self):
        category = Category.objects.create(name='Electronics')
        assert Category.objects.count() == 1
        assert category.name == 'Electronics'

    @pytest.mark.django_db
    def test_name_field_cannot_be_empty(self):
        with pytest.raises(ValidationError):
            Category.objects.create(name="")

    @pytest.mark.django_db
    def test_name_field_cannot_exceed_200_characters(self):
        name = 'a' * 201
        with pytest.raises(ValidationError):
            Category.objects.create(name=name)

    @pytest.mark.django_db
    def test_name_field_can_be_200_characters(self):
        name = 'a' * 200
        category = Category.objects.create(name=name)
        assert category.name == name

    @pytest.mark.django_db
    def test_can_save_category_with_parent(self):
        parent_category = Category.objects.create(name="Parent Category")
        child_category = Category.objects.create(name="Child Category",
                                                 parent=parent_category)
        assert child_category.parent == parent_category
