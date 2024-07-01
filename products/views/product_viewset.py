from rest_framework import status, viewsets, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.db import transaction
from products.models import Product, Category, Image, Unit
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
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

                response_data = serializer.data.copy()
                response_data['categories'] = category_names
                response_data['unit'] = unit_name

                return Response(response_data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def handle_categories(self, categories_data) -> list[int]:
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
        if image_file:
            Image.objects.create(product=product, image_file=image_file)

    def handle_unit(self, unit_data) -> int:
        if unit_data:
            try:
                unit = Unit.objects.get(name=unit_data)
                unit_id = unit.id
                return unit_id
            except Unit.DoesNotExist as exc:
                raise NotFound(detail=f"Unit '{unit_data}' not found") from exc
        raise NotFound(detail="Unit cannot be empty")
