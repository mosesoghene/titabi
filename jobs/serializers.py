from rest_framework import serializers
from django.contrib.gis.geos.point import Point

from accounts.serilizers import UserSerializer, PublicUserSerializer
from artisans.models import ArtisanProfile
from artisans.serializers import ArtisanProfileSerializer
from .models import JobRequest


class JobRequestSerializer(serializers.ModelSerializer):
    created_by = PublicUserSerializer(read_only=True)
    artisan = PublicUserSerializer(source='artisan.user', read_only=True)
    target_artisan_id = serializers.IntegerField(required=False, write_only=True)

    # Read-only output of location
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    # Accept input
    lat = serializers.FloatField(write_only=True, required=True)
    lon = serializers.FloatField(write_only=True, required=True)

    target_artisan = ArtisanProfileSerializer(read_only=True)

    class Meta:
        model = JobRequest
        fields = [
            'id', 'created_by', 'artisan',
            'target_artisan', 'target_artisan_id', 'category', 'description',
            'status', 'lat', 'lon', 'latitude', 'longitude',
        ]
        read_only_fields = [
            'status', 'created_at', 'updated_at',
            'target_artisan', 'latitude', 'longitude'
        ]

    def validate_target_artisan_id(self, value):
        if not ArtisanProfile.objects.filter(id=value).exists():
            raise serializers.ValidationError("Target artisan does not exist.")
        return value

    def get_latitude(self, obj):
        return obj.location.y if obj.location else None

    def get_longitude(self, obj):
        return obj.location.x if obj.location else None

    def create(self, validated_data):
        from django.contrib.gis.geos import Point

        lat = validated_data.pop('lat')
        lon = validated_data.pop('lon')
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
    user = PublicUserSerializer(read_only=True)
    category = serializers.StringRelatedField()
    skills = serializers.StringRelatedField(many=True)
    distance = serializers.SerializerMethodField()
    rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ArtisanProfile
        fields = [
            'id', 'user', 'category', 'skills',
            'experience_years', 'available', 'distance',
            'rating', 'rating_count',
        ]

    def get_user(self, obj):
        u = obj.user
        return {
            'id': u.id,
            'full_name': f"{u.first_name} {u.last_name}".strip() or None,
            'email': u.email,
            'phone_number': u.phone_number,
        }

    def get_distance(self, obj):
        return round(obj.distance.km, 2) if getattr(obj, 'distance', None) else None


