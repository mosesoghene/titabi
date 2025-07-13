from django.db import models
from django.conf import settings
from jobs.models import JobRequest
from artisans.models import ArtisanProfile

# Create your models here.
class Rating(models.Model):
    job = models.OneToOneField(JobRequest, on_delete=models.CASCADE, related_name='rating')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artisan = models.ForeignKey(ArtisanProfile, on_delete=models.CASCADE, related_name='ratings')

    rating = models.PositiveSmallIntegerField()  # e.g. 1 to 5
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating}★ - {self.artisan} by {self.reviewer}'