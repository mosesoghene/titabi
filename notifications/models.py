from django.db import models
from django.conf import settings

class FCMDevice(models.Model):
    """Firebase Cloud Messaging API Model to store device token information for notifications."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)