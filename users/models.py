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
from django.core.validators import RegexValidator


class CustomerUser(AbstractUser):
    """Custom user model representing user profiles with extended fields.

    This model extends the default Django user model (`AbstractUser`) with
    additional fields for user profile management, including date of birth,
    phone number, shipping address and billing address.
    """
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9*+#-]+$',
                message=('Phone number can only contain '
                         'digits (0-9) and symbols (*+#-).'),
                code='invalid_phone_number'
            )
        ]
    )
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_customers',  # Custom related_name for groups
        blank=True,
        verbose_name='groups',
        help_text=('The groups this user belongs to. A user will get'
                   'all permissions granted to each of their groups.')
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        # Custom related_name for user_permissions
        related_name='user_customers',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

    def __str__(self) -> str:
        """Return the username as the string representation of the user."""
        return f'{self.username}'
