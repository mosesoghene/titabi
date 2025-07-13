from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FCMDevice


class RegisterFCMTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "Token is required."}, status=400)

        device, created = FCMDevice.objects.update_or_create(
            user=request.user,
            defaults={"token": token}
        )
        return Response({"detail": "FCM token registered."})