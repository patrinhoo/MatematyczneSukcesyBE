from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "given_name",
            "last_name",
            "password",
            "password2",
            "role",
            "terms_confirmed",
        ]

    def validate(self, attrs):
        email = attrs["email"].lower()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                {"email": "A user with this email already exists."}
            )
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        if not attrs["terms_confirmed"]:
            raise serializers.ValidationError(
                {"terms_confirmed": "You have to confirm terms."}
            )
        return attrs

    def create(self, validated_data: dict):
        password = validated_data.pop("password", None)
        validated_data.pop("password2", None)

        user = get_user_model().objects.create(**validated_data)

        user.set_password(password)
        user.save()

        return user


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


class ManageUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "given_name",
            "last_name",
            "password",
            "password2",
            "role",
            "terms_confirmed",
            "gender",
            "avatar",
        ]

    def validate(self, attrs):
        password = attrs.get("password", None)
        password2 = attrs.get("password2", None)

        if password and password != password2:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs


class BasicUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "given_name",
            "last_name",
            "avatar",
        ]
