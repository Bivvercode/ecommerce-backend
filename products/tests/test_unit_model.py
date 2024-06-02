"""
This module contains test cases for the Unit model in the products application.

Tests cover the creation and validation of units, including validation of
the unit's name and symbol fields.

Each test case is a method on the TestUnitModel class, and uses
the pytest.mark.django_db decorator to ensure that the database
is properly set up and torn down for each test.
"""

import pytest
from django.core.exceptions import ValidationError
from products.models import Unit


class TestUnitModel:
    """Test cases for the Unit model."""

    @pytest.mark.django_db
    def test_create_unit(self):
        """Test the creation of a unit."""
        unit = Unit.objects.create(name='Kilogram', symbol='kg')
        assert Unit.objects.count() == 1
        assert unit.name == 'Kilogram'
        assert unit.symbol == 'kg'

    @pytest.mark.django_db
    def test_name_field_is_required(self):
        """Test that the name field is required."""
        with pytest.raises(ValidationError):
            Unit.objects.create(symbol='kg')

    @pytest.mark.django_db
    def test_symbol_field_is_required(self):
        """Test that the symbol field is required."""
        with pytest.raises(ValidationError):
            Unit.objects.create(name='Kilogram')

    @pytest.mark.django_db
    def test_name_field_cannot_exceed_200_characters(self):
        """Test that the name field cannot exceed 200 characters."""
        name = 'a' * 201
        with pytest.raises(ValidationError):
            Unit.objects.create(name=name, symbol='kg')

    @pytest.mark.django_db
    def test_symbol_field_cannot_exceed_9_characters(self):
        """Test that the symbol field cannot exceed 9 characters."""
        symbol = 'a' * 10
        with pytest.raises(ValidationError):
            Unit.objects.create(name='Kilogram', symbol=symbol)
