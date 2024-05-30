"""
This module contains API views related to password management
in a Django application.

It includes a view for changing the password of an
authenticated user (ChangePasswordView).

This view uses Django's built-in authentication system and
Django Rest Framework's token-based authentication.

Classes:
    ChangePasswordView: API view to change the password of an authenticated
                        user. It checks the old password, validates the
                        new password, and if everything is correct,
                        it changes the password.
"""
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import views, permissions, status
from rest_framework.response import Response


class ChangePasswordView(views.APIView):
    """
    API view to change the password of an authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Change the password of the authenticated user.

        This method checks the old password, validates the new password,
        and if everything is correct, it changes the password. If there are
        any issues, it returns an error response.
        """
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {"detail": "Both old and new passwords must be provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response({"old_password": ["Wrong password."]},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"new_password": list(e.messages)},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password changed successfully"},
                        status=status.HTTP_200_OK)
