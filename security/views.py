from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from .models import RecoverPassword  
from .serializers import (CustomUserLoginSerializer, 
UserRegisterSerializer, PasswordRecoverySerializer, 
OtpValidationSerializer, ResetPasswordSerializer
)


# Login Custumizado
class CustomUserLoginView(CreateAPIView):
    serializer_class = CustomUserLoginSerializer
    permission_classes = [AllowAny] 

    CACHE_KEY_PREFIX = "login"
    @method_decorator(cache_page(300, key_prefix=CACHE_KEY_PREFIX))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': access_token,
            'refresh': refresh_token,
        }

        return Response(response_data, status=status.HTTP_200_OK)

# Register User Custumized
class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

# Recovery Password
class PasswordRecoveryView(CreateAPIView):
    serializer_class = PasswordRecoverySerializer

# OTP code Recevy
class OtpValidationView(CreateAPIView):
    serializer_class = OtpValidationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # reset_url = serializer.validated_data["reset_url"]
        # return Response({"message": "OTP validado com sucesso", "reset_url": reset_url})
        token_value = serializer.validated_data["token"]
        return Response({"message": "OTP validado com sucesso", "token": token_value})


# Reset Password After OTP
class ResetPasswordView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def get_object(self, uuid, token):
        try:
            return get_object_or_404(RecoverPassword, id=uuid, token=token, is_used=False)
        except Http404:
            raise NotFound(detail="O link de redefinição de senha é inválido ou expirou.", code=404)


    def post(self, request, uuid, token):
        recover_data = self.get_object(uuid, token)

        serializer = self.get_serializer(recover_data, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response({"message": "Senha redefinida com sucesso."})




