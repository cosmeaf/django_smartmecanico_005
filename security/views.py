from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, PasswordRecoverySerializer, OtpValidationSerializer, ResetPasswordSerializer
from .models import RecoverPassword  
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound

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


class PasswordRecoveryView(CreateAPIView):
    serializer_class = PasswordRecoverySerializer


class OtpValidationView(CreateAPIView):
    serializer_class = OtpValidationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_url = serializer.validated_data["reset_url"]
        return Response({"message": "OTP validado com sucesso", "reset_url": reset_url})


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





