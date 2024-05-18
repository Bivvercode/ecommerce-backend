from rest_framework import views, permissions, status
from rest_framework.response import Response
from users.models import CustomerUser


class ProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
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
        user: CustomerUser = request.user
        data = request.data

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.shipping_address = data.get('shipping_address',
                                         user.shipping_address)
        user.billing_address = data.get('billing_address',
                                        user.billing_address)

        user.save()

        return Response({"detail": "Profile updated"},
                        status=status.HTTP_200_OK)
