from rest_framework import serializers
from django.contrib.gis.geos.point import Point

from accounts.serilizers import UserSerializer
from artisans.models import ArtisanProfile
from artisans.serializers import ArtisanProfileSerializer
from .models import JobRequest


class JobRequestSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    target_artisan_id = serializers.IntegerField(required=False, write_only=True)

    target_artisan = ArtisanProfileSerializer(read_only=True)

    class Meta:
        model = JobRequest
        fields = [
            'id', 'category', 'description',
            'latitude', 'longitude',
            'target_artisan_id', 'target_artisan',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at', 'target_artisan']

    def validate_target_artisan_id(self, value):
        if not ArtisanProfile.objects.filter(id=value).exists():
            raise serializers.ValidationError("Target artisan does not exist.")
        return value

    def create(self, validated_data):
        from django.contrib.gis.geos import Point

        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        validated_data['location'] = Point(lon, lat)
        validated_data['created_by'] = self.context['request'].user

        target_id = validated_data.pop('target_artisan_id', None)
        if target_id:
            validated_data['target_artisan'] = ArtisanProfile.objects.get(id=target_id)

        return super().create(validated_data)


class JobStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequest
        fields = ['status']
        read_only_fields = []

    def validate_status(self, value):
        user = self.context['request'].user
        job = self.instance

        if user.is_artisan:
            if value not in ['in_progress', 'completed']:
                raise serializers.ValidationError("Artisans can only set in_progress or completed.")
        else:
            if value != 'cancelled':
                raise serializers.ValidationError("You can only cancel your own jobs.")

        if job.status == 'completed':
            raise serializers.ValidationError("This job is already completed.")
        return value


class ArtisanProfilePublicSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = serializers.StringRelatedField()
    skills = serializers.StringRelatedField(many=True)
    distance = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = [
            'id', 'user', 'category', 'skills',
            'experience_years', 'available', 'distance'
        ]

    def get_distance(self, obj):
        if hasattr(obj, 'distance') and obj.distance:
            return round(obj.distance.km, 2)
        return None

