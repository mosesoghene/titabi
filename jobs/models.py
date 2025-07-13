from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.utils.translation import gettext_lazy as _

from artisans.models import ArtisanCategory, ArtisanProfile


# Create your models here.
class JobStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    ACCEPTED = 'accepted', _('Accepted')
    IN_PROGRESS = 'in_progress', _('In Progress')
    COMPLETED = 'completed', _('Completed')
    CANCELLED = 'cancelled', _('Cancelled')


class JobRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_requests'
    )
    artisan = models.ForeignKey(
        ArtisanProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_jobs'
    )
    category = models.ForeignKey(
        ArtisanCategory, on_delete=models.SET_NULL, null=True
    )
    description = models.TextField()
    location = geomodels.PointField(geography=True)

    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    target_artisan = models.ForeignKey(
        ArtisanProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='direct_requests'
    )

    def __str__(self):
        return f"Job by {self.created_by.username} - {self.status}"