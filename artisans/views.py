from rest_framework.generics import ListAPIView
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q
from rest_framework import generics, permissions

from jobs.serializers import ArtisanProfilePublicSerializer
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


class ArtisanSearchView(ListAPIView):
    serializer_class = ArtisanProfilePublicSerializer

    def get_queryset(self):
        qs = ArtisanProfile.objects.select_related('user', 'category').prefetch_related('skills').filter(user__is_active=True)

        # 🔍 Keyword search (by name, phone, email)
        query = self.request.query_params.get('q')
        if query:
            qs = qs.filter(
                Q(user__phone_number__icontains=query) |
                Q(user__email__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )

        # 🧰 Filter by category ID
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category__id=category_id)

        # 🛠️ Filter by skill ID
        skill_id = self.request.query_params.get('skill')
        if skill_id:
            qs = qs.filter(skills__id=skill_id)

        # 📍 Optional location + radius filtering
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius = self.request.query_params.get('radius', 10)

        if lat and lon:
            point = Point(float(lon), float(lat))
            qs = qs.filter(location__distance_lte=(point, D(km=float(radius)))).annotate(distance=Distance('location', point)).order_by('distance')

        return qs




