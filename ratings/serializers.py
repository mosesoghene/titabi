from rest_framework import serializers
from .models import Rating
from artisans.models import ArtisanProfile
from jobs.models import JobRequest

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'job', 'artisan', 'rating', 'review', 'created_at']
        read_only_fields = ['id', 'created_at', 'artisan']

    def validate(self, data):
        job = data['job']
        user = self.context['request'].user

        if job.created_by != user:
            raise serializers.ValidationError("You can only rate jobs you created.")

        if job.status != 'completed':
            raise serializers.ValidationError("You can only rate completed jobs.")

        if hasattr(job, 'rating'):
            raise serializers.ValidationError("This job has already been rated.")

        return data

    def create(self, validated_data):
        rating = super().create(validated_data)

        artisan = rating.artisan
        all_ratings = artisan.ratings.all()
        artisan.rating = round(sum(r.rating for r in all_ratings) / all_ratings.count(), 2)
        artisan.rating_count = all_ratings.count()
        artisan.save()

        return rating

