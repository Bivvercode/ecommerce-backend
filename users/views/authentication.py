from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from users.models import CustomerUser
from users.serializers import CustomerUserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomerUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerUserSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None

    def perform_create(self, serializer):
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        self.token = token.key

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'token': self.token,
        }
        return response
