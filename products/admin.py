from django.contrib import admin
from .models import (Unit, Category, Product, ProductCategory,
                     Image, Cart, CartItem, Wishlist)

admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Image)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
