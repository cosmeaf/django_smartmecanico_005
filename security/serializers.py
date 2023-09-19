import uuid
from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from .models import RecoverPassword  
from .utils.emails.auth_security import send_email_otp
from .utils.machine.get_data_machine import get_machine_info
from .utils.location.get_location_info import get_location_info
import os
import base64
import random
import requests



class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='E-mail', max_length=254)
    password = serializers.CharField(label="Password", 
                                     write_only=True, 
                                     required=True,
                                     style={'input_type': 'password'}, min_length=8, max_length=128,
                                     validators=[password_validation.validate_password])
    passconf = serializers.CharField(label="Confirm Password", 
                                     write_only=True,
                                     style={'input_type': 'password'}, min_length=8, max_length=128,
                                     required=True)


    class Meta:
        model = User
        fields = ['email', 'password', 'passconf']

    def validate(self, data):
            if data.get('password') != data.get('passconf'):
                raise serializers.ValidationError('As senhas não coincidem.')
            
            email = data.get('email')

            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError('Endereço de email já está em uso.')

            return data

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['email'],
            email = validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail', max_length=254)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError('E-mail não encontrado')

        otp_code = str(random.randint(100000, 999999))
        token = base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8')

        ip_address = requests.get('https://api.ipify.org').text
        
        # Definindo a data e hora de expiração para 1 hora a partir de agora
        expiry_datetime = timezone.now() + timezone.timedelta(hours=1)

        RecoverPassword.objects.update_or_create(
            user=user, 
            defaults={
                'otp': otp_code, 
                'expiry_datetime': expiry_datetime, 
                'token': uuid.uuid4(), 
                'ip_address': ip_address,
                'is_used': False
            }
        )

        machine_info = get_machine_info()  
        location_info = get_location_info(ip_address)
        #send_email_otp(user, otp_code, machine_info, location_info) 
        return value

    def create(self, validated_data):
        return validated_data


class OtpValidationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(label="OTP Code", max_length=6, write_only=True)

    class Meta:
        model = RecoverPassword
        fields = ('otp',)

    def validate(self, data):
        try:
            otp_data = RecoverPassword.objects.get(otp=data['otp'])
        except RecoverPassword.DoesNotExist:
            raise serializers.ValidationError('O OTP é inválido.')

        if otp_data.is_used:
            raise serializers.ValidationError('Este OTP já foi utilizado.')

        if timezone.now() > otp_data.expiry_datetime:
            raise serializers.ValidationError('O OTP expirou.')

        reset_url = reverse('password_reset', kwargs={'uuid': str(otp_data.id), 'token': otp_data.token})
        
        return {"reset_url": reset_url}


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(label="Password", 
                                     write_only=True, 
                                     required=True,
                                     style={'input_type': 'password'}, min_length=8, max_length=128,
                                     validators=[password_validation.validate_password])
    passconf = serializers.CharField(label="Confirm Password", 
                                     write_only=True, 
                                     style={'input_type': 'password'}, min_length=8, max_length=128,
                                     required=True)

    def validate(self, data):
        if data['password'] != data['passconf']:
            raise serializers.ValidationError("As senhas não correspondem.")
        return data

    def update(self, instance, validated_data):
        instance.user.set_password(validated_data['password'])
        instance.user.save()

        instance.is_used = True
        instance.expiry_datetime = timezone.now()
        instance.save()

        return instance
