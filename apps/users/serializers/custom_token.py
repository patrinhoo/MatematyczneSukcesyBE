from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs["email"] = attrs["email"].lower()
        user = get_user_model().objects.filter(email__iexact=attrs["email"]).first()

        if user:
            if not user.check_password(attrs["password"]):
                raise AuthenticationFailed("The password you entered is incorrect.")
            if not user.is_active:
                raise AuthenticationFailed("Your account is not active.")

        return super().validate(attrs)
