
import re
from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    def validate(self, password, _user=None):
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
        return ('Your password must contain at least 1 uppercase letter, '
                'at least 1 lowercase letter, at least 1 digit, and '
                'at least 1 special character.')
