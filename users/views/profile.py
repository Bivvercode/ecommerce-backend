"""
This module contains API views related to user
profile management in the application.

It includes a view for retrieving and updating the profile
of an authenticated user (ProfileView).

This view uses Django's built-in authentication system and
Django Rest Framework's token-based authentication.

Classes:
    ProfileView: API view to retrieve and update the profile
                 of an authenticated user. It includes methods for
                 getting the current profile data (get) and updating
                 the profile data (put).
"""
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from users.serializers import CustomerUserSerializer
from users.models import CustomerUser


class ProfileView(views.APIView):
    """
    API view to retrieve and update the profile of an authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Retrieve the profile of the authenticated user.
        """
        user: CustomerUser = request.user

        data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'shipping_address': user.shipping_address,
            'billing_address': user.billing_address,
        }

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update the profile of the authenticated user.
        """
        user: CustomerUser = request.user
        serializer = CustomerUserSerializer(
            user,
            data=request.data,
            partial=True
        )

        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Profile updated"},
                                status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
