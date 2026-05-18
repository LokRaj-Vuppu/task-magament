from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=3)
    confirm_password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(
        required=True, allow_null=False, allow_blank=False
    )
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
            "full_name",
            "access",
            "refresh",
        ]

    extra_kwargs = {"access": {"read_only": True}, "refresh": {"read_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data["full_name"],
        )

        return user

    def get_access(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_refresh(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {"access": str(refresh.access_token), "refresh": str(refresh)}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def save(self):
        refresh_token = self.validated_data["refresh"]

        token = RefreshToken(refresh_token)
        token.blacklist()
