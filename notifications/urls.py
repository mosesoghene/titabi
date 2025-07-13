from django.urls import path

from notifications.views import RegisterFCMTokenView

urlpatterns = [

    path("fcm/register/", RegisterFCMTokenView.as_view()),
]