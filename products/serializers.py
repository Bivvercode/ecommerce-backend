"""
This module defines serializers for various models in the application.
Serializers are responsible for converting models into JSON format
for API responses, and for validating and deserializing
input data to Django model instances.

The serializers cover a range of models including Unit, Category,
Product, ProductCategory, Image, Cart, CartItem, and Wishlist.
Each serializer handles the intricacies of its respective
model, such as managing many-to-many relationships, custom
field serialization, and image URL construction.

Each serializer is equipped with custom methods as needed to
support the unique requirements of the application's data
representation and manipulation.
"""
from rest_framework import serializers
from .models import (Unit, Category, Product,
                     ProductCategory, Image, Cart,
                     CartItem, Wishlist)


class UnitSerializer(serializers.ModelSerializer):
    """
    Serializer for Unit model. Converts Unit instances into
    JSON format and vice versa.
    """
    class Meta:
        model = Unit
        fields = ['id', 'name', 'symbol']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model. Handles conversion of
    Category instances toJSON format and back, including
    handling of hierarchical relationships if present.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model. Manages serialization of Product instances,
    including related fields like unit and categories. Provides custom fields
    to represent detailed views of related objects
    and handles image URL construction.
    """
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )
    categories_details = serializers.SerializerMethodField()
    unit_details = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price',
                  'discount', 'unit', 'quantity_per_unit',
                  'currency', 'categories', 'unit_details',
                  'categories_details', 'image_url']

    def get_categories_details(self, obj):
        """
        Returns detailed information for each category
        associated with the product.
        """
        return [{'id': category.id, 'name': category.name}
                for category in obj.categories.all()]

    def get_image_url(self, obj):
        """
        Constructs and returns the absolute URL for the product's image.
        """
        request = self.context.get('request')
        try:
            image_instance = Image.objects.get(product=obj)
        except Image.DoesNotExist:
            return None
        return request.build_absolute_uri(image_instance.image_file.url)

    def get_unit_details(self, obj):
        """
        Returns detailed information for the unit associated with the product.
        """
        return {'id': obj.unit.id, 'name': obj.unit.name,
                'symbol': obj.unit.symbol}

    def to_internal_value(self, data):
        """
        Custom method to handle conversion of input data into a format
        suitable for creating or updating Product instances,
        particularly for handling categories as
        a list or comma-separated values.
        """
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
        """
        Custom create method to handle the creation of
        Product instances, including setting categories.
        """
        categories_data = validated_data.pop('categories', [])
        product = Product.objects.create(**validated_data)
        product.categories.set(categories_data)
        return product

    def update(self, instance, validated_data):
        """
        Custom update method to handle updating Product
        instances, including updating categories.
        """
        categories_data = validated_data.pop('categories', None)
        if categories_data is not None:
            instance.categories.set(categories_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Custom method to modify the default serialization behavior,
        particularly to exclude certain fields from the output representation.
        """
        ret = super().to_representation(instance)
        ret.pop('categories', None)
        ret.pop('unit', None)
        return ret


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for ProductCategory model. Handles serialization
    of ProductCategory instances, which represent the
    many-to-many relationship between products and categories.
    """
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
    """
    Serializer for Image model. Manages serialization of Image instances,
    including constructing absolute URLs for image files.
    """
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'image_file', 'product', 'image_url']

    def get_image_url(self, obj):
        """
        Constructs and returns the absolute URL for an image file.
        """
        request = self.context.get('request')
        image_url = obj.image_file.url
        return request.build_absolute_uri(image_url)


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart model. Handles serialization of
    Cart instances, representing a user's shopping cart.
    """
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem model. Manages serialization of CartItem
    instances, which represent individual items within a
    shopping cart, including product and quantity.
    """
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
    """
    Serializer for Wishlist model. Handles serialization of
    Wishlist instances, representing a user's
    collection of desired products.
    """
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products']
