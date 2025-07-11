from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)
    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


