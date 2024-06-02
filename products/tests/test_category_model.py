"""
This module contains test cases for the Category model in the products app.

Tests cover the creation of categories, validation of the name field, and
the ability to create a category with a parent category.

Each test case is a method on the TestCategoryModel class, and uses
the pytest.mark.django_db decorator to ensure that the database
is properly set up and torn down for each test.
"""
import pytest
from django.core.exceptions import ValidationError
from products.models import Category


class TestCategoryModel:
    """Test cases for the Category model."""

    @pytest.mark.django_db
    def test_create_category(self):
        """Test that a category can be created with a name."""
        category = Category.objects.create(name='Electronics')
        assert Category.objects.count() == 1
        assert category.name == 'Electronics'

    @pytest.mark.django_db
    def test_name_field_cannot_be_empty(self):
        """Test that a category cannot be created with an empty name."""
        with pytest.raises(ValidationError):
            Category.objects.create(name="")

    @pytest.mark.django_db
    def test_name_field_cannot_exceed_200_characters(self):
        """
        Test that a category cannot be created with a name
        longer than 200 characters.
        """
        name = 'a' * 201
        with pytest.raises(ValidationError):
            Category.objects.create(name=name)

    @pytest.mark.django_db
    def test_name_field_can_be_200_characters(self):
        """
        Test that a category can be created with a name
        of exactly 200 characters.
        """
        name = 'a' * 200
        category = Category.objects.create(name=name)
        assert category.name == name

    @pytest.mark.django_db
    def test_can_save_category_with_parent(self):
        """Test that a category can be created with a parent category."""
        parent_category = Category.objects.create(name="Parent Category")
        child_category = Category.objects.create(name="Child Category",
                                                 parent=parent_category)
        assert child_category.parent == parent_category
