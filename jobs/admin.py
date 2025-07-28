from django.contrib import admin

from accounts.serilizers import UserSerializer
from .models import JobRequest

# Register your models here.
@admin.register(JobRequest)
class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_display = (
        'id', 'created_by', 'artisan', 'category',
        'description', 'location', 'status',
        'created_at', 'updated_at', 'target_artisan'
    )