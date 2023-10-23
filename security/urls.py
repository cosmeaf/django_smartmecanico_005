from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from rest_framework.routers import DefaultRouter
from .views import CustomUserLoginView, RegisterView, OtpValidationView, PasswordRecoveryView, ResetPasswordView


router = DefaultRouter()
# router.register(r'users', CustomUserModelViewSet, basename='users')
# router.register(r'addresses', AddressModelViewSet, basename='addresses')
# router.register(r'vehicles', VehicleModelViewSet, basename='vehicles')

urlpatterns = [
    #path('login/', csrf_exempt(ratelimit(key='user', rate='5/m', method='POST')(views.CustomUserLoginView.as_view())), name='login'),
    path('', include(router.urls)),
    re_path(r'', include(router.urls)),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-recovery/', PasswordRecoveryView.as_view(), name='password_recovery'),
    path('otp-validation/', OtpValidationView.as_view(), name='otp_validation'),
    path('password-reset/<uuid:uuid>/<str:token>/', ResetPasswordView.as_view(), name='password_reset'),
]