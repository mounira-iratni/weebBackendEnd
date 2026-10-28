"""Routing for authentication endpoints."""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PasswordResetConfirmView, PasswordResetRequestView, SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", TokenObtainPairView.as_view(), name="signin"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("reset-password/request/", PasswordResetRequestView.as_view(), name="reset_password_request"),
    path("reset-password/confirm/", PasswordResetConfirmView.as_view(), name="reset_password_confirm"),
]
