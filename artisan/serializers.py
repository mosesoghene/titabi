from rest_framework import serializers
from .models import ArtisanCategory, ArtisanProfile
from django.contrib.gis.geos import Point

class ArtisanCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanCategory
        fields = ['id', 'name']


class ArtisanProfileSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = [
            'category', 'available', 'skills',
            'experience_years', 'latitude', 'longitude'
        ]

    def get_latitude(self, obj):
        return obj.location.y if obj.location else None

    def get_longitude(self, obj):
        return obj.location.x if obj.location else None

    def update(self, instance, validated_data):
        lat = validated_data.pop('latitude', None)
        lon = validated_data.pop('longitude', None)

        if lat is not None and lon is not None:
            instance.location = Point(lon, lat)  # (lon, lat) order

        return super().update(instance, validated_data)