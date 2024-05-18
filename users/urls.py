from django.urls import path
from .views import authentication, profile, passwords

urlpatterns = [
    path('register/', authentication.RegisterView.as_view(), name='register'),
    path('login/', authentication.LoginView.as_view(), name='login'),
    path('logout/', authentication.LogoutView.as_view(), name='logout'),

    path('profile/', profile.ProfileView.as_view(), name='profile'),

    path('password/change/', passwords.ChangePasswordView.as_view(),
         name='change_password'),
]
