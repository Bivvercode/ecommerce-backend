"""
This module configures the Django admin site for the models in the application.

It registers the Unit, Category, Product, ProductCategory, Image, Cart,
CartItem, and Wishlist models with the admin site, allowing them
to be managed through the Django admin interface.

Operations:
    - Register the Unit model with the admin site.
    - Register the Category model with the admin site.
    - Register the Product model with the admin site.
    - Register the ProductCategory model with the admin site.
    - Register the Image model with the admin site.
    - Register the Cart model with the admin site.
    - Register the CartItem model with the admin site.
    - Register the Wishlist model with the admin site.
"""
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
