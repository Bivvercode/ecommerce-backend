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
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (RegexValidator, EmailValidator,
                                    validate_email)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomerUser(AbstractUser):
    """Custom user model representing user profiles with extended fields.

    This model extends the default Django user model (`AbstractUser`) with
    additional fields for user profile management, including date of birth,
    phone number, shipping address and billing address.
    """
    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[
            EmailValidator(message='Please enter a valid email address.')
        ]
    )
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

    def validate_password_complexity(self, value: str):
        """Validate password complexity."""
        if len(value) < 8:
            raise ValidationError(
                'Password needs to be at least 8 chatacters long.'
            )

        if not any(char.isupper() for char in value):
            raise ValidationError(
                'Password must contain at least one uppercase letter.'
            )

        if not any(char.islower() for char in value):
            raise ValidationError(
                'Password must contain at least one lowercase letter.'
            )

        if not any(char.isdigit() for char in value):
            raise ValidationError(
                'Password must contain at least one digit.'
            )

        if not any(char in string.punctuation for char in value):
            raise ValidationError(
                'Password must contain at least one symbol.'
            )

    def validate_username_complexity(self, value: str):
        """Validate username complexity."""
        if len(value) < 4:
            raise ValidationError(
                'Username must be at least 4 characters long.'
            )

        if len(value) > 20:
            raise ValidationError(
                'Username cannot be more than 20 characters long.'
            )

    def validate_phone_number_complexity(self, value: str):
        """Validate phone number complexity."""
        if len(value) > 20:
            raise ValidationError(
                'Phone number cannot be more than 20 characters long.'
            )

    def clean(self):
        super().clean()

        if not self.username:
            raise ValidationError("Name cannot be empty.")

        if not self.email:
            raise ValidationError('Email cannot be empty.')

        if not self.password:
            raise ValidationError('Password cannot be empty.')

        if not self.first_name:
            raise ValidationError('First name cannot be empty.')

        if not self.last_name:
            raise ValidationError('Last name cannot be empty.')

        self.validate_password_complexity(self.password)
        self.validate_username_complexity(self.username)
        self.validate_phone_number_complexity(self.phone_number)

        validate_email(self.email)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return the username as the string representation of the user."""
        return f'{self.username}'
