from rest_framework import serializers
from accounts.models import User
from artisans.models import ArtisanProfile
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    phone_number = serializers.CharField(required=True)
    is_artisan = serializers.BooleanField(required=False)
    email = serializers.EmailField(required=False)

    def get_cleaned_data(self):
        return {
            'phone_number': self.validated_data.get('phone_number'),
            'password1': self.validated_data.get('password1'),
            'email': self.validated_data.get('email', ''),
            'is_artisan': self.validated_data.get('is_artisan', False)
        }

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email', '')
        user.is_artisan = self.cleaned_data.get('is_artisan', False)
        user.save()

        if user.is_artisan:
            ArtisanProfile.objects.get_or_create(user=user)

        return user


class ChooseRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=[('artisan', 'Artisan'), ('user', 'User')])

    def save(self, **kwargs):
        user = self.context['request'].user
        role = self.validated_data['role']

        if role == 'artisan':
            user.is_artisan = True
            user.save()
            ArtisanProfile.objects.get_or_create(user=user)
        else:
            user.is_artisan = False
            user.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'email', 'is_artisan']
        read_only_fields = ['phone_number']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email']