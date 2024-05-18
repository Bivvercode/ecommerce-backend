from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from users.models import CustomerUser
from users.serializers import CustomerUserSerializer
from django.db import transaction


class RegisterView(generics.CreateAPIView):
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
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Wrong Credentials"},
                        status=status.HTTP_400_BAD_REQUEST)
