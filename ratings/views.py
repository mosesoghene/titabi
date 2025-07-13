from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Rating
from .serializers import RatingSerializer

# Create your views here.
class CreateRatingView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        serializer.save(
            reviewer=self.request.user,
            artisan=job.artisan
        )