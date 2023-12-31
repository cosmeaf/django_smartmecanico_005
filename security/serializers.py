import os
import base64
import random
import requests
import uuid
from rest_framework import serializers
from django.contrib.auth import authenticate, password_validation
from django.utils import timezone
from datetime import datetime, timedelta
from django.urls import reverse
from .models import CustomUser, RecoverPassword
from security.signals import user_created_signal
from .utils.machine.get_data_machine import get_client_info
from .utils.location.get_location_info import get_location_info
from .utils.otp_handler import create_or_update_recovery_data
import logging
logger = logging.getLogger(__name__)


MAX_FAILED_ATTEMPTS = 5
LOCKOUT_TIME = 15

class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail', max_length=254)
    password = serializers.CharField(
        label="Password",
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        validators=[password_validation.validate_password]
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("E-mail não registrado.")

        user_authenticated = authenticate(username=email, password=password)

        if user_authenticated:
                user.failed_login_attempts = 0
                user.save()
                data['user'] = user
        else:
            # Incrementar tentativas falhadas e definir a última tentativa falhada
            user.failed_login_attempts += 1
            user.last_failed_login = datetime.now()
            user.save()

            if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                lockout_time = timedelta(minutes=LOCKOUT_TIME)
                current_time = datetime.now()

                if user.last_failed_login and (current_time - user.last_failed_login) > lockout_time:
                    user.failed_login_attempts = 0
                    user.save()
                else:
                    raise serializers.ValidationError("Muitas tentativas de login. Tente novamente em {} minutos.".format(LOCKOUT_TIME))

            raise serializers.ValidationError(
                "Unable to log in with provided credentials.",
                code='authentication_failed'
            )

        return data

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(label='First Name', max_length=30)
    last_name = serializers.CharField(label='Last Name', max_length=30)
    email = serializers.EmailField(label='E-mail', max_length=254)
    password = serializers.CharField(
        label="Password",
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        validators=[password_validation.validate_password]
    )
    passconf = serializers.CharField(
        label="Confirm Password",
        write_only=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'passconf']

    def is_valid(self, raise_exception=False):
        is_valid = super(UserRegisterSerializer, self).is_valid(raise_exception=False)

        if not is_valid and 'non_field_errors' in self.errors:
            custom_errors = {}
            custom_errors['error'] = self.errors['non_field_errors'][0]
            self._errors = custom_errors

            if raise_exception:
                raise serializers.ValidationError(self.errors)

        return is_valid

    def validate(self, data):
        if data.get('password') != data.get('passconf'):
            raise serializers.ValidationError('As senhas não coincidem.')

        email = data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Endereço de email já está em uso.')

        return data

    def create(self, validated_data):
        validated_data.pop('passconf')

        ip_address = self.context['request'].META.get('REMOTE_ADDR')
        machine_info = get_client_info(self.context['request'])
        location_info = get_location_info(ip_address)

        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        user_created_signal.send(
            sender=self.__class__, 
            instance=user, 
            ip_address=ip_address, 
            machine_info=machine_info, 
            location_info=location_info
        )

        return user


class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail', max_length=254)

    def validate_email(self, value):
        user = CustomUser.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError('E-mail não encontrado')

        ip_address = self.context['request'].META.get('REMOTE_ADDR')
        machine_info = get_client_info(self.context['request'])

        # Uso da função para criar ou atualizar os dados de recuperação
        recovery_data = create_or_update_recovery_data(user, ip_address, machine_info)

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

        # reset_url = reverse('password_reset', kwargs={'uuid': str(otp_data.id), 'token': otp_data.token})
        # logger.info(reset_url)
        # return {"reset_url": reset_url}
        token_value = f"{str(otp_data.id)}/{otp_data.token}"
        logger.info(token_value)
        return {"token": token_value}



class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        label="Password",
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        validators=[password_validation.validate_password]
    )
    passconf = serializers.CharField(
        label="Confirm Password",
        write_only=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        required=True
    )

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
