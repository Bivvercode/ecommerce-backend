"""
This module contains the configuration for the 'products' Django app.

Classes:
    ProductsConfig: Configuration for the 'products' Django app.
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
