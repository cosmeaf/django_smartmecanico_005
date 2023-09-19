from django.urls import path
from .views import RegisterView, OtpValidationView, PasswordRecoveryView, ResetPasswordView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('password-recovery/', PasswordRecoveryView.as_view(), name='password_recovery'),
    path('otp-validation/', OtpValidationView.as_view(), name='otp_validation'),
    path('password-reset/<uuid:uuid>/<str:token>/', ResetPasswordView.as_view(), name='password_reset'),
]
