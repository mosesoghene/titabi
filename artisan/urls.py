from django.urls import path
from .views import ArtisanCategoryListView, ArtisanProfileUpdateView

urlpatterns = [
    path('categories/', ArtisanCategoryListView.as_view(), name='artisan-categories'),
    path('profile/', ArtisanProfileUpdateView.as_view(), name='artisan-profile'),
]