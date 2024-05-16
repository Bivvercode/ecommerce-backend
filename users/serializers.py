from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomerUser


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomerUser(**validated_data)
        if password:
            validate_password(password, user)
            user.set_password(password)
        else:
            raise serializers.ValidationError("Password field is required")
        user.save()
        return user
