import base64
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from django.core.files.base import ContentFile
from products.models import Product, Category, Image
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(commit=False)

            self.handle_categories(product, request.data.get('categories', []))
            self.handle_image_upload(product, request.data.get('image'))

            serializer = self.get_serializer(product)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def handle_categories(self, product, categories_data):
        if categories_data:
            categories = [Category.objects.get_or_create(name=category_name)[0]
                          for category_name in categories_data]
            product.categories.set(categories)

    def handle_image_upload(self, product, image_data):
        if image_data:
            image_format, imgstr = image_data.split(';base64,')
            ext = image_format.split('/')[-1]
            image_file = ContentFile(
                base64.b64decode(imgstr), name=f'{product.name}.{ext}'
            )
            Image.objects.create(image_file=image_file, product=product)
