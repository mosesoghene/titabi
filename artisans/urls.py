from django.urls import path
from .views import ArtisanCategoryListView, ArtisanProfileDetailUpdateView

urlpatterns = [
    path('categories/', ArtisanCategoryListView.as_view(), name='artisan-categories'),
    path('profile/', ArtisanProfileDetailUpdateView.as_view(), name='artisan-profile'),
]