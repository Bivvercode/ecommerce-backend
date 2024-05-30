"""
This module configures the Django admin site for the CustomerUser model.

It registers the CustomerUser model with the admin site, allowing it
to be managed through the Django admin interface.

Operations:
    - Register the CustomerUser model with the admin site.
"""
from django.contrib import admin
from .models import CustomerUser

admin.site.register(CustomerUser)
