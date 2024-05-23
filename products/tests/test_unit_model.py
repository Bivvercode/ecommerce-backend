import pytest
from django.core.exceptions import ValidationError
from products.models import Unit


class TestUnitModel:
    """Test cases for the Unit model."""

    @pytest.mark.django_db
    def test_create_unit(self):
        unit = Unit.objects.create(name='Kilogram', symbol='kg')
        assert Unit.objects.count() == 1
        assert unit.name == 'Kilogram'
        assert unit.symbol == 'kg'

    @pytest.mark.django_db
    def test_name_field_is_required(self):
        with pytest.raises(ValidationError):
            Unit.objects.create(symbol='kg')

    @pytest.mark.django_db
    def test_symbol_field_is_required(self):
        with pytest.raises(ValidationError):
            Unit.objects.create(name='Kilogram')

    @pytest.mark.django_db
    def test_name_field_cannot_exceed_200_characters(self):
        name = 'a' * 201
        with pytest.raises(ValidationError):
            Unit.objects.create(name=name, symbol='kg')

    @pytest.mark.django_db
    def test_symbol_field_cannot_exceed_9_characters(self):
        symbol = 'a' * 10
        with pytest.raises(ValidationError):
            Unit.objects.create(name='Kilogram', symbol=symbol)
