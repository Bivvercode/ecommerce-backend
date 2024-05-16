from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomerUser


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        required_fields = ['username', 'email',
                           'first_name', 'last_name',
                           'password']
        for field in required_fields:
            if field not in attrs:
                raise serializers.ValidationError(
                    {field: f'{field} field is required.'}
                )
        password = attrs.get('password')
        user = CustomerUser(**attrs)
        try:
            validate_password(password, user)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomerUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
