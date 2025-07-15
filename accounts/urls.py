from django.urls import path
from .views import UpdateUserProfileView, ChooseRoleView
from accounts.views import CustomLoginView, CustomRegisterView

urlpatterns = [
    path('auth/login/', CustomLoginView.as_view(), name='custom-login'),
    path('auth/register/', CustomRegisterView.as_view(), name='custom-register'),
    path('me/', UpdateUserProfileView.as_view(), name='user-profile'),
    path('choose-role/', ChooseRoleView.as_view(), name='choose-role'),
]