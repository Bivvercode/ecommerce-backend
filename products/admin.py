"""
This module configures the Django admin site for the models in
the application by registering each model along with its
custom ModelAdmin class. These customizations include configurations
for how the models are displayed and managed in the Django admin interface,
such as specifying the fields to be displayed in the list view,
enabling filters, and setting up search capabilities.

Custom ModelAdmin classes are defined and registered for the following models:
    - Unit: Customizes the display of units in the admin.
    - Category: Customizes the display of categories in the admin.
    - Product: Customizes the display and management of products,
               including filters by availability and category.
    - ProductCategory: Customizes the display of product categories,
                       including filters by category.
    - Image: Customizes the display of images, associated with products.
    - Cart: Customizes the display of carts, including search by user.
    - CartItem: Customizes the display of cart items, including filters
                by cart and product.
    - Wishlist: Customizes the display of wishlists, including search by user.

These customizations aim to enhance the usability and efficiency of
the admin interface for managing the application's data.
"""
from django.contrib import admin
from .models import (Unit, Category, Product, ProductCategory,
                     Image, Cart, CartItem, Wishlist)


class UnitAdmin(admin.ModelAdmin):
    """
    Admin interface options for Unit model.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface options for Category model.
    """
    list_display = ('name',)
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface options for Product model.
    """
    list_display = ('name', 'price', 'available', 'category')
    list_filter = ('available', 'category')
    search_fields = ('name', 'description')


class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface options for ProductCategory model.
    """
    list_display = ('product', 'category')
    list_filter = ('category',)
    search_fields = ('product__name', 'category__name')


class ImageAdmin(admin.ModelAdmin):
    """
    Admin interface options for Image model.
    """
    list_display = ('product', 'image')
    search_fields = ('product__name',)


class CartAdmin(admin.ModelAdmin):
    """
    Admin interface options for Cart model.
    """
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)


class CartItemAdmin(admin.ModelAdmin):
    """
    Admin interface options for CartItem model.
    """
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')
    search_fields = ('cart__user__username', 'product__name')


class WishlistAdmin(admin.ModelAdmin):
    """
    Admin interface options for Wishlist model.
    """
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)


admin.site.register(Unit, UnitAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)
