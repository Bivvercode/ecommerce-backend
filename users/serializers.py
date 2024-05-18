import re
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import CustomerUser


class CustomerUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[0-9*+#-]+$',
                message=('Phone number can only contain '
                         'digits (0-9) and symbols (*+#-).'),
                code='invalid_phone_number'
            )
        ],
        required=False,
        allow_blank=True
    )

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password', 'phone_number',
                  'shipping_address', 'billing_address']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        required_fields = ['email', 'first_name', 'last_name']
        if self.instance is None:  # This is a create operation
            required_fields.extend(['username', 'password'])
        for field in required_fields:
            if field not in attrs:
                raise serializers.ValidationError(
                    {field: f'{field} field is required.'}
                )
        password = attrs.get('password')
        if password or self.instance is None:
            user = CustomerUser(**attrs)
            try:
                validate_password(password, user)
            except ValidationError as e:
                raise serializers.ValidationError({'password': e.messages})
        return attrs

    def update(self, instance, validated_data):
        self.validate(validated_data)

        password = validated_data.pop('password', None)
        phone_number = validated_data.pop('phone_number', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        if phone_number:
            if not re.match(r'^[0-9*+#-]+$', phone_number):
                raise serializers.ValidationError(
                    {'phone_number':
                     ('Phone number can only contain '
                      'digits (0-9) and symbols (*+#-).')}
                )
            instance.phone_number = phone_number

        instance.save()
        return instance

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomerUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
