"""
This module defines the URL routes for the 'users' Django app.

The routes include:
    - Register: A route for user registration.
    - Login: A route for user login.
    - Logout: A route for user logout.
    - Profile: A route for retrieving and updating the profile
               of an authenticated user.
    - Change Password: A route for changing the password
                       of an authenticated user.
"""
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
