from django.contrib.auth.models import AbstractUser
from django.db import models

class UserAccount(AbstractUser):
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True) 
    def __str__(self):
        return self.username