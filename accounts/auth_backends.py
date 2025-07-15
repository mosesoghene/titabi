from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

User = get_user_model()
class PhoneOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None

        # Try to normalize if it looks like a phone number
        normalized_phone = self._normalize_phone(username)

        try:
            user = User.objects.get(
                Q(phone_number=normalized_phone) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def _normalize_phone(self, value):
        try:
            parsed = phonenumbers.parse(value, None)
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.E164
                )
        except NumberParseException:
            pass
        return value  # fallback to original if it's not a phone
