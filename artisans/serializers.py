from rest_framework import serializers

from accounts.serilizers import UserSerializer
from .models import ArtisanCategory, ArtisanProfile, ArtisanSkill
from django.contrib.gis.geos import Point

class ArtisanSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanSkill
        fields = ['id', 'name']

class ArtisanCategorySerializer(serializers.ModelSerializer):
    skills = ArtisanSkillSerializer(many=True, read_only=True)

    class Meta:
        model = ArtisanCategory
        fields = ['id', 'name', 'skills']


class ArtisanProfileSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ArtisanSkill.objects.all()
    )
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = ArtisanProfile
        fields = [
            'category', 'skills', 'available', 'experience_years',
            'latitude', 'longitude'
        ]

    def update(self, instance, validated_data):
        from django.contrib.gis.geos import Point
        lat = validated_data.pop('latitude', None)
        lon = validated_data.pop('longitude', None)
        if lat and lon:
            instance.location = Point(lon, lat)
        return super().update(instance, validated_data)


