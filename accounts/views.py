from rest_framework import generics, permissions
from accounts.serilizers import UserProfileSerializer, ChooseRoleSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Create your views here.
class UpdateUserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChooseRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChooseRoleSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Role updated successfully.'})