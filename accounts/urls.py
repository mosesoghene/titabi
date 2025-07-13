from django.urls import path
from .views import UpdateUserProfileView, ChooseRoleView

urlpatterns = [
    path('me/', UpdateUserProfileView.as_view(), name='user-profile'),
    path('choose-role/', ChooseRoleView.as_view(), name='choose-role'),
]