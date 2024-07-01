from rest_framework import serializers
from .models import (Unit, Category, Product,
                     ProductCategory, Image, Cart,
                     CartItem, Wishlist)


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name', 'symbol']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price',
                  'discount', 'unit', 'quantity_per_unit',
                  'currency', 'categories']

    def to_internal_value(self, data):
        categories = data.get('categories', '')
        if isinstance(categories, str):
            try:
                categories_ids = [int(id_str) for id_str
                                  in categories.split(',')]
            except ValueError as exc:
                raise serializers.ValidationError(
                    {'categories':
                     'Categories must be a comma-separated list of IDs.'}
                ) from exc
        elif isinstance(categories, list):
            try:
                categories_ids = [int(id) for id in categories]
            except ValueError as exc:
                raise serializers.ValidationError(
                    {'categories': 'Categories must be a list of IDs.'}
                ) from exc
        else:
            raise serializers.ValidationError(
                {'categories': 'Invalid format for categories.'}
            )

        data.setlist('categories', categories_ids)
        return super().to_internal_value(data)

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        product = Product.objects.create(**validated_data)
        product.categories.set(categories_data)
        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', None)
        if categories_data is not None:
            instance.categories.set(categories_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProductCategorySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = ProductCategory
        fields = ['id', 'product', 'category']


class ImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = Image
        fields = ['id', 'image_file', 'product']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all()
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']


class WishlistSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products']
