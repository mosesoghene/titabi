from django.conf import settings
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class ArtisanCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ArtisanSkill(models.Model):
    category = models.ForeignKey(ArtisanCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class ArtisanProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(ArtisanCategory, on_delete=models.SET_NULL, null=True)
    skills = models.ManyToManyField(ArtisanSkill, blank=True)
    location = geomodels.PointField(geography=True, null=True, blank=True)
    available = models.BooleanField(default=True)
    experience_years = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} ({self.category.name if self.category else "Uncategorized"})'
