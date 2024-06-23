"""
This module contains the configuration for the 'orders' Django app.

Classes:
    OrdersConfig: Configuration for the 'orders' Django app.
"""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Configuration for the 'orders' Django app.

    Attributes:
        default_auto_field: Specifies the type of auto-created primary key
                            field for models without an explicit primary key.
        name: The name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
