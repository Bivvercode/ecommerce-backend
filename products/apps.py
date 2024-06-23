"""
This module contains the configuration for the 'products' Django app.

Classes:
    ProductsConfig: Configuration for the 'products' Django app.
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Configuration for the 'products' Django app.

    Attributes:
        default_auto_field: Specifies the type of auto-created primary key
                            field for models without an explicit primary key.
        name: The name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
