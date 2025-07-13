from django.contrib import admin

from artisans.models import ArtisanProfile, ArtisanCategory

# Register your models here.
admin.site.register(ArtisanProfile)
admin.site.register(ArtisanCategory)