from django.shortcuts import render
from rest_framework import generics, permissions
from .models import ArtisanCategory, ArtisanProfile
from .serializers import ArtisanCategorySerializer, ArtisanProfileSerializer

# Create your views here.

class ArtisanCategoryListView(generics.ListAPIView):
    queryset = ArtisanCategory.objects.prefetch_related('skills').all()
    serializer_class = ArtisanCategorySerializer
    permission_classes = [permissions.AllowAny]


class ArtisanProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ArtisanProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return ArtisanProfile.objects.get(user=self.request.user)