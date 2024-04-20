from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomerUser(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)
