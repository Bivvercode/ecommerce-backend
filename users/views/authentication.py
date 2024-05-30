"""
This module contains API views for user authentication in the application.

It includes views for registering a new user (RegisterView),
logging in an existing user (LoginView), and
logging out a currently authenticated user (LogoutView).

These views use Django's built-in authentication system
and Django Rest Framework's token-based authentication.

Classes:
    RegisterView: API view to register a new user. It creates a new user,
                  assigns them to a group, and generates a token for them.
    LoginView: API view to authenticate a user. It checks the provided
               username and password, and if they are valid, it returns
               a token for the user.
    LogoutView: API view to logout a user. It deletes the token of the
                authenticated user.
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from users.models import CustomerUser
from users.serializers import CustomerUserSerializer


class RegisterView(generics.CreateAPIView):
    """
    API view to register a new user.
    """
    queryset = CustomerUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerUserSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        self.user = None

    def perform_create(self, serializer):
        with transaction.atomic():
            self.user = serializer.save()

            group, created = Group.objects.get_or_create(name='user_customers')
            self.user.groups.add(group)

            content_type = ContentType.objects.get_for_model(CustomerUser)

            permission, created = Permission.objects.get_or_create(
                codename='user_customers',
                content_type=content_type,
            )

            if created:
                permission.name = 'User Customers'
                permission.save()

            self.user.user_permissions.add(permission)

            self.user.save()

            self.user.refresh_from_db()

            self.token, created = Token.objects.get_or_create(user=self.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'token': self.token.key,
        }
        return response


class LoginView(views.APIView):
    """
    API view to login a user.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Authenticate the user and return the token.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Wrong Credentials"},
                        status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    """
    API view to logout a user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Delete the token of the authenticated user.
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
