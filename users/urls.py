from django.urls import path
from .views import authentication

urlpatterns = [
    path('register/', authentication.RegisterView.as_view(), name='register'),
    path('login/', authentication.LoginView.as_view(), name='login'),
    path('logout/', authentication.LogoutView.as_view(), name='logout'),
]
