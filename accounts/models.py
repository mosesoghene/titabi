from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number or self.email or f"User {self.pk}")