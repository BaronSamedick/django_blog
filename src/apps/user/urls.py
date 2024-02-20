from django.urls import path

from .views import (
    ProfileDetailView,
    ProfileUpdateView,
    UserForgotPasswordView,
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    UserPasswordResetConfirmView,
    UserRegisterView,
)

urlpatterns = [
    path("user/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("user/<str:slug>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("change-password/", UserPasswordChangeView.as_view(), name="change_password"),
    path("reset-password/", UserForgotPasswordView.as_view(), name="password_reset"),
    path("set-new-password/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
