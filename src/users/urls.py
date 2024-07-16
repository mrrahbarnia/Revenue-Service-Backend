from django.urls import path

from . import apis

app_name = "users"


urlpatterns = [
    path("register/", apis.UserRegisterApi.as_view(), name="register"),
    path("verify-account/", apis.UserVerifyAccountApi.as_view(), name="verify_account"),
    path("resend-verification/", apis.UserResendVerificationApi.as_view(), name="resend_verification"),
    path("login/", apis.MyTokenObtainPairView.as_view(), name="login"),
    path("change-password/", apis.UserChangePassword.as_view(), name="change_password"),
    path("reset-password/", apis.UserResetPasswordApi.as_view(), name="reset_password"),
    path("reset-password/verify/", apis.UserVerifyResetPasswordApi.as_view(), name="verify_reset_password"),
]
