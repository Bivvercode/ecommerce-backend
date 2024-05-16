from django.urls import path
from .views import authentication

urlpatterns = [
    path('register/', authentication.RegisterView.as_view(), name='register'),
]
