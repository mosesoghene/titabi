from django.urls import path
from .views import CreateJobRequestView, ListUserJobRequestsView, NearbyJobsView, AcceptJobView, UpdateJobStatusView, \
    ArtisanJobHistoryView, DirectJobRequestsView, DeclineJobView, JobMatchView, SuggestArtisanView, JobRequestDetailView

urlpatterns = [
    path('create/', CreateJobRequestView.as_view(), name='create-job'),
    path('my-jobs/', ListUserJobRequestsView.as_view(), name='my-jobs'),
    path('nearby/', NearbyJobsView.as_view(), name='nearby-jobs'),
    path('<int:pk>/accept/', AcceptJobView.as_view(), name='accept-job'),
    path('<int:pk>/update-status/', UpdateJobStatusView.as_view(), name='update-job-status'),
    path('my-jobs/artisan/', ArtisanJobHistoryView.as_view(), name='artisan-job-history'),
    path('direct-requests/', DirectJobRequestsView.as_view(), name='direct-job-requests'),
    path('<int:pk>/decline/', DeclineJobView.as_view(), name='decline-job'),
    path('<int:pk>/match/', JobMatchView.as_view(), name='job-match'),
    path('<int:pk>/suggest/<int:artisan_id>/', SuggestArtisanView.as_view(), name='suggest-artisan'),
    path('<int:pk>/', JobRequestDetailView.as_view(), name='job-detail'),
]
