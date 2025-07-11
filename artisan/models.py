from django.conf import settings
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)
    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class ArtisanCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ArtisanProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(ArtisanCategory, on_delete=models.SET_NULL, null=True)
    location = geomodels.PointField(geography=True, null=True, blank=True)
    available = models.BooleanField(default=True)
    skills = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0, max_length=5.0)

    def __str__(self):
        return f'{self.user.username} ({self.category.name if self.category else "Uncategorized"})'
