"""API views for authentication endpoints."""

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
	PasswordResetConfirmSerializer,
	PasswordResetRequestResponseSerializer,
	PasswordResetRequestSerializer,
	SignUpSerializer,
	build_reset_tokens_for_email,
)


class SignUpView(APIView):
	"""Register a new user account in inactive state."""

	permission_classes = [permissions.AllowAny]

	def post(self, request):
		"""Create a user and return a moderation-related message."""
		serializer = SignUpSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(
			{
				"message": (
					"Account created successfully. "
					"An administrator must validate your account before login."
				)
			},
			status=status.HTTP_201_CREATED,
		)


class PasswordResetRequestView(APIView):
	"""Generate reset token information from an email address."""

	permission_classes = [permissions.AllowAny]

	def post(self, request):
		"""Return uid/token to allow frontend reset confirmation flow."""
		serializer = PasswordResetRequestSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		tokens = build_reset_tokens_for_email(serializer.validated_data["email"])
		if not tokens:
			return Response(
				{"message": "If this email exists, a reset link can be generated."},
				status=status.HTTP_200_OK,
			)

		response_serializer = PasswordResetRequestResponseSerializer(tokens)
		return Response(response_serializer.data, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
	"""Validate reset data and set a new password."""

	permission_classes = [permissions.AllowAny]

	def post(self, request):
		"""Confirm password reset and persist the new password."""
		serializer = PasswordResetConfirmSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(
			{"message": "Password reset successful."},
			status=status.HTTP_200_OK,
		)
