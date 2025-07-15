from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from accounts.models import User
from artisans.models import ArtisanProfile
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    is_artisan = serializers.BooleanField(required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'phone_number',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'is_artisan'
        ]

    def validate_phone_number(self, value):
        try:
            parsed = phonenumbers.parse(value, "NG")
            if not phonenumbers.is_valid_number(parsed):
                raise serializers.ValidationError("Invalid phone number.")
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['password1'])
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        is_artisan = validated_data.pop('is_artisan', False)

        user = User(**validated_data)
        user.set_password(password)
        user.is_artisan = is_artisan
        user.save()

        if is_artisan:
            ArtisanProfile.objects.get_or_create(user=user)

        return user


class CustomLoginSerializer(LoginSerializer):
    login = serializers.CharField(help_text="Phone number or email")
    password = serializers.CharField(write_only=True)

    def validate_login(self, value):
        try:
            parsed = phonenumbers.parse(value, "NG")
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.E164
                )
        except NumberParseException:
            pass

        return value.strip()  # fallback: use as-is

    def validate(self, data):
        login = self.validate_login(data.get("login"))
        password = data.get("password")

        user = authenticate(username=login, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data

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