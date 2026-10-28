"""Serializers for authentication workflows."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Validate and create an inactive user waiting for admin approval."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def validate_password(self, value):
        """Apply Django password validation rules."""
        validate_password(value)
        return value

    def create(self, validated_data):
        """Create user with is_active=False until admin validation."""
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save(update_fields=["password", "is_active"])
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """Input payload for starting the password reset flow."""

    email = serializers.EmailField()


class PasswordResetRequestResponseSerializer(serializers.Serializer):
    """Response payload for frontend reset page integration."""

    uid = serializers.CharField()
    token = serializers.CharField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Validate a reset token and set a new password."""

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        """Ensure uid/token pair matches an existing user."""
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uid"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError({"uid": "Invalid reset uid."})

        if not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        attrs["user"] = user
        return attrs

    def validate_new_password(self, value):
        """Apply Django password rules for reset flow as well."""
        validate_password(value)
        return value

    def save(self, **kwargs):
        """Persist the newly provided password for the resolved user."""
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


def build_reset_tokens_for_email(email: str):
    """Return uid/token for a user email, or None if user does not exist."""
    user = User.objects.filter(email=email).first()
    if not user:
        return None

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return {"uid": uid, "token": token}
