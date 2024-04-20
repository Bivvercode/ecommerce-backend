"""Custom user model for the users app.

This module defines a custom user model named `CustomerUser` for
the users app in the Django project. The `CustomerUser` model
extends the default Django user model (`AbstractUser`) with additional fields
to enhance user profiles and authentication capabilities.

The `CustomerUser` model includes fields such as `date_of_birth`,
`phone_number`, `shipping_address`, and `billing_address` to
provide comprehensive user profile management.

Classes:
    CustomerUser: Custom user model representing user profiles
    with extended fields.

Usage:
    Import the `CustomerUser` model into other parts of the Django project
    for user authentication, registration, and profile management.

Example:
    from users.models import CustomerUser

    # Create a new user instance
    user = CustomerUser.objects.create(username='john_doe',
                                        email='john@example.com')
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomerUser(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)
