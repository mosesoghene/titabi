from rest_framework import generics, permissions
from accounts.serilizers import UserProfileSerializer, ChooseRoleSerializer, CustomRegisterSerializer, \
    CustomLoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from dj_rest_auth.views import LoginView
# from dj_rest_auth.registration.views import RegisterView
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.generics import CreateAPIView


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


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'login': {'type': 'string', 'example': '+2348012345678 or user@example.com'},
                    'password': {'type': 'string', 'format': 'password'},
                },
                'required': ['login', 'password']
            }
        },
        responses={200: OpenApiExample(
            'Success',
            value={"access": "jwt_token", "refresh": "refresh_token"},
            response_only=True
        )}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomRegisterView(CreateAPIView):
    serializer_class = CustomRegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'phone_number': {
                        'type': 'string',
                        'example': '+2348012345678'
                    },
                    'email': {
                        'type': 'string',
                        'format': 'email',
                        'example': 'user@example.com'
                    },
                    'first_name': {
                        'type': 'string',
                        'example': 'Ada'
                    },
                    'last_name': {
                        'type': 'string',
                        'example': 'Obi'
                    },
                    'password1': {
                        'type': 'string',
                        'format': 'password',
                        'example': 'supersecure123'
                    },
                    'password2': {
                        'type': 'string',
                        'format': 'password',
                        'example': 'supersecure123'
                    },
                    'is_artisan': {
                        'type': 'boolean',
                        'example': True
                    },
                },
                'required': [
                    'phone_number',
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2'
                ]
            }
        },
        responses={201: OpenApiExample(
            'Success',
            value={"detail": "Verification e-mail sent."},
            response_only=True
        )}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
