"""
This module defines the viewset for the Product model, handling the creation,
retrieval, update, and deletion of product instances via API requests.
It supports multipart form data to accommodate file uploads for product images,
and it uses transactional operations to ensure data integrity during create
and update actions. The viewset also includes custom handling for related
objects such as categories and units, ensuring they are properly associated
with the product instances.
"""
from rest_framework import status, viewsets, permissions
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from products.models import Product, Category, Image, Unit
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Extends the default ModelViewSet from Django REST Framework to provide
    custom behavior for handling Product instances. This includes overriding
    the `create` and `update` methods to support multipart form data,
    and to ensure atomic transactions for data integrity. Custom methods
    for handling related objects like categories and units are also defined.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        """
        Overrides the default `create` method to handle multipart form data.
        This method processes not only the standard fields for a Product
        instance but also includes custom handling for categories, unit,
        and image file uploads, requiring specific implementation details
        for these fields. Ensures atomic transactions for data integrity.
        """
        with transaction.atomic():
            category_names = request.data.getlist('categories', [])
            unit_name = request.data.get('unit', None)

            categories = self.handle_categories(category_names)
            unit = self.handle_unit(unit_name)

            request_data = request.data.copy()
            request_data['categories'] = categories
            request_data['unit'] = unit

            serializer = self.get_serializer(data=request_data)
            if serializer.is_valid():
                product = serializer.save()

                self.handle_image_upload(product, request.FILES.get('image'))

                serializer = self.get_serializer(product)
                headers = self.get_success_headers(serializer.data)

                return Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Overrides the default `update` method to handle multipart form data,
        including the standard fields for a Product instance. This method
        also includes custom handling for updating categories, unit, and
        managing image file replacement, highlighting the need for specific
        implementation for these fields in an atomic transaction.
        """
        with transaction.atomic():
            pk = kwargs.get('pk')
            product = get_object_or_404(Product, pk=pk)

            category_names = request.data.getlist('categories', [])
            unit_name = request.data.get('unit', None)

            categories = self.handle_categories(category_names)
            unit = self.handle_unit(unit_name)

            request_data = request.data.copy()
            request_data['categories'] = categories
            request_data['unit'] = unit

            serializer = self.get_serializer(
                product,
                data=request_data,
                partial=True
            )

            if serializer.is_valid():
                product = serializer.save()

                new_image = request.FILES.get('image')
                print(request.FILES)
                if new_image:
                    try:
                        old_image = Image.objects.get(product=product)
                        old_image.image_file.delete(save=False)
                        old_image.delete()
                    except Image.DoesNotExist:
                        pass
                    self.handle_image_upload(product, new_image)

                serializer = self.get_serializer(product)
                headers = self.get_success_headers(serializer.data)

                return Response(serializer.data,
                                status=status.HTTP_200_OK,
                                headers=headers)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def handle_categories(self, categories_data) -> list[int]:
        """
        Custom method to process category names from
        the request into category IDs.
        """
        if categories_data:
            categories = []
            for name in categories_data:
                try:
                    category = Category.objects.get(name=name)
                    categories.append(category.id)
                except Category.DoesNotExist as exc:
                    raise NotFound(
                        detail=f"Category '{name}' not found"
                    ) from exc
            return categories
        return []

    def handle_image_upload(self, product, image_file) -> None:
        """
        Custom method to handle the upload of an image file
        for a Product instance.
        """
        if image_file:
            Image.objects.create(product=product, image_file=image_file)

    def handle_unit(self, unit_data) -> int:
        """
        Custom method to convert a unit name from the request into a unit ID.
        """
        if unit_data:
            try:
                unit = Unit.objects.get(name=unit_data)
                unit_id = unit.id
                return unit_id
            except Unit.DoesNotExist as exc:
                raise NotFound(detail=f"Unit '{unit_data}' not found") from exc
        raise NotFound(detail="Unit cannot be empty")
