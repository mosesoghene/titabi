from artisans import serializers
from artisans.models import ArtisanProfile

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