"""
This module contains a custom password validator for the application.

The validator checks that a password meets certain complexity
requirements, including containing at least one uppercase letter,
one lowercase letter, one digit, and one special character.

Classes:
    CustomPasswordValidator: Custom password validator. It includes
                             methods for validating a password (validate)
                             and getting the help text for the
                             validator(get_help_text).
"""
import re
from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    """
    Custom password validator.

    This validator checks that a password meets certain complexity
    requirements, including containing at least one uppercase letter,
    one lowercase letter, one digit, and one special character.
    """
    def validate(self, password, _user=None):
        """
        Validate a password.

        This method checks that the password contains at least
        one uppercase letter, one lowercase letter, one digit, and
        one special character. If the password does not meet
        these requirements, it raises a ValidationError.
        """
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                'Password must contain at least 1 uppercase letter.'
            )
        if not re.findall('[a-z]', password):
            raise ValidationError(
                'Password must contain at least 1 lowercase letter.'
            )
        if not re.findall('[0-9]', password):
            raise ValidationError(
                'Password must contain at least 1 digit.'
            )
        if not re.findall('[^A-Za-z0-9]', password):
            raise ValidationError(
                'Password must contain at least 1 special character.'
            )

    def get_help_text(self):
        """
        Get the help text for this validator.

        This method returns a string that explains the password requirements.
        """
        return ('Your password must contain at least 1 uppercase letter, '
                'at least 1 lowercase letter, at least 1 digit, and '
                'at least 1 special character.')
