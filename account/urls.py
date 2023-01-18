from django.urls import path
from account.views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SendPassEmailView,
    UserPassResetView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("change-pass/", UserChangePasswordView.as_view(), name="change_pass"),
    path("pass_email/", SendPassEmailView.as_view(), name="pass_email"),
    path("pass-reset/<uid>/<token>/", UserPassResetView.as_view(), name="pass_reset"),
]
