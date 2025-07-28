from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from artisans.models import ArtisanProfile
from artisans.serializers import ArtisanProfileSerializer
from .models import JobRequest, JobStatus
from .serializers import JobRequestSerializer, JobStatusUpdateSerializer, ArtisanProfilePublicSerializer


# Create your views here.
class AcceptJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user

        if not user.is_artisan or not hasattr(user, 'artisanprofile'):
            return Response({'detail': 'Only artisans can accept jobs.'}, status=403)

        job = get_object_or_404(JobRequest, pk=pk)

        if job.created_by == user:
            return Response({'detail': 'You cannot accept your own job.'}, status=403)

        if job.status != JobStatus.PENDING or job.artisan is not None:
            return Response({'detail': 'Job is already taken.'}, status=400)

        if job.target_artisan and job.target_artisan != user.artisanprofile:
            return Response({'detail': 'This job was directed to someone else.'}, status=403)

        job.artisan = user.artisanprofile
        job.status = 'accepted'
        job.save()

        return Response({'detail': 'Job accepted successfully.'}, status=200)


class DeclineJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        if not user.is_artisan or not hasattr(user, 'artisanprofile'):
            return Response({'detail': 'Only artisans can decline jobs.'}, status=403)

        job = get_object_or_404(JobRequest, pk=pk)

        if job.created_by == user:
            return Response({'detail': 'You cannot decline your own job.'}, status=403)

        if job.status != 'pending' or job.artisan is not None:
            return Response({'detail': 'Job is already accepted or closed.'}, status=400)

        if job.target_artisan != user.artisanprofile:
            return Response({'detail': 'You can only decline jobs directed to you.'}, status=403)

        # Clear target so others can now claim
        job.target_artisan = None
        job.save()

        return Response({'detail': 'You have declined this job. It is now public again.'}, status=200)


class ArtisanJobHistoryView(ListAPIView):
    serializer_class = JobRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_artisan or not hasattr(user, 'artisanprofile'):
            return JobRequest.objects.none()

        queryset = JobRequest.objects.filter(artisan=user.artisanprofile)

        # Optional filter: /jobs/my-jobs/artisan/?status=completed
        status_param = self.request.query_params.get('status')
        if status_param and status_param in JobStatus.values:
            queryset = queryset.filter(status=status_param)

        return queryset.order_by('-updated_at')


class CreateJobRequestView(generics.CreateAPIView):
    queryset = JobRequest.objects.all()
    serializer_class = JobRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


class ListUserJobRequestsView(generics.ListAPIView):
    serializer_class = JobRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = JobRequest.objects.filter(created_by=self.request.user)
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset.order_by('-updated_at')


class NearbyJobsView(ListAPIView):
    serializer_class = JobRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'artisanprofile', None)
        if not user.is_artisan or not profile:
            return JobRequest.objects.none()

        lat_q = self.request.query_params.get('lat')
        lon_q = self.request.query_params.get('lon')

        if lat_q and lon_q:
            lat = float(lat_q)
            lon = float(lon_q)
        elif profile.location:
            lat = profile.location.y
            lon = profile.location.x
        else:
            return JobRequest.objects.none()

        radius = float(self.request.query_params.get('radius', 10))
        point = Point(lon, lat)

        public_jobs = JobRequest.objects.filter(
            artisan__isnull=True,
            category=profile.category,
            location__distance_lte=(point, D(km=radius)),
            status='pending'
        ).exclude(created_by=user)

        direct_jobs = JobRequest.objects.filter(
            artisan__isnull=True,
            status='pending',
            target_artisan=profile
        )

        return (public_jobs | direct_jobs).distinct().order_by('-created_at')


class DirectJobRequestsView(ListAPIView):
    serializer_class = JobRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_artisan or not hasattr(user, 'artisanprofile'):
            return JobRequest.objects.none()

        return JobRequest.objects.filter(
            target_artisan=user.artisanprofile,
            status='pending',
            artisan__isnull=True
        ).order_by('-created_at')


class UpdateJobStatusView(generics.UpdateAPIView):
    serializer_class = JobStatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_artisan:
            return JobRequest.objects.filter(artisan__user=user)

        if job.status == JobStatus.COMPLETED:
            raise serializers.ValidationError("This job is already completed.")
        return JobRequest.objects.filter(created_by=user)


class JobMatchView(ListAPIView):
    serializer_class = ArtisanProfilePublicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        job = get_object_or_404(JobRequest, pk=self.kwargs['pk'])

        if job.artisan is not None or job.status != JobStatus.PENDING:
            return ArtisanProfile.objects.none()

        # Optional: filter by skill
        required_skills = job.category.skills.all()

        qs = ArtisanProfile.objects.filter(
            category=job.category,
            user__is_active=True,
        ).exclude(user=job.created_by)

        # Optional: radius filter
        radius = float(self.request.query_params.get('radius', 10))
        qs = qs.annotate(distance=Distance('location', job.location))
        qs = qs.filter(location__distance_lte=(job.location, D(km=radius)))

        return qs.order_by('distance')


class SuggestArtisanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, artisan_id):
        user = request.user
        job = get_object_or_404(JobRequest, pk=pk)

        # Only the creator of the job can suggest
        if job.created_by != user:
            return Response({'detail': 'You can only suggest for your own job.'}, status=403)

        if job.status != JobStatus.PENDING:
            return Response({'detail': 'Job is not open for suggestions.'}, status=400)

        artisan = get_object_or_404(ArtisanProfile, pk=artisan_id)

        # Optional: only allow one suggestion per job
        if job.target_artisan:
            return Response({'detail': 'This job already has a suggested artisan.'}, status=400)

        # Assign target_artisan
        job.target_artisan = artisan
        job.save()

        return Response({'detail': 'Artisan suggested successfully.'}, status=200)


class JobRequestDetailView(generics.RetrieveAPIView):
    queryset = JobRequest.objects.all()
    serializer_class = JobRequestSerializer
    permission_classes = [IsAuthenticated]