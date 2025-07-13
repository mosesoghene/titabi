from django.urls import path
from .views import CreateRatingView

urlpatterns = [
    path('create/', CreateRatingView.as_view(), name='create-rating'),
]