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
    user = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=ArtisanProfile._meta.get_field('category').related_model.objects.all()
    )
    category_name = serializers.SerializerMethodField()

    skills = serializers.ListField(child=serializers.CharField(), write_only=True)
    skill_names = serializers.SerializerMethodField()

    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = ArtisanProfile
        fields = [
            'user', 'category', 'category_name',
            'skills', 'skill_names',
            'available', 'experience_years',
            'latitude', 'longitude',
        ]

    def get_user(self, obj):
        u = obj.user
        return {
            'id': u.id,
            'full_name': f"{u.first_name} {u.last_name}".strip() or None,
            'email': u.email,
            'phone_number': u.phone_number,
        }

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_skill_names(self, obj):
        return [s.name for s in obj.skills.all()]

    def update(self, instance, validated_data):
        lat = validated_data.pop('latitude', None)
        lon = validated_data.pop('longitude', None)
        skill_names = validated_data.pop('skills', [])

        if lat is not None and lon is not None:
            instance.location = Point(lon, lat)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if instance.category and skill_names is not None:
            new_skills = []
            for raw in skill_names:
                norm = raw.strip().lower()
                skill, _ = ArtisanSkill.objects.get_or_create(
                    category=instance.category,
                    name__iexact=norm,
                    defaults={'name': norm.title(), 'category': instance.category}
                )
                new_skills.append(skill)
            instance.skills.set(new_skills)

        return instance

