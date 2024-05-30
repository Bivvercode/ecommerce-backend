"""
This module contains the configuration for the 'users' Django app.

Classes:
    UsersConfig: Configuration for the 'users' Django app.
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the 'users' Django app.

    Attributes:
        default_auto_field: Specifies the type of auto-created primary key
                            field for models without an explicit primary key.
        name: The name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
