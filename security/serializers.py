import os
import base64
import random
import requests
import uuid
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.utils import timezone
from django.urls import reverse
from .models import CustomUser, RecoverPassword  
from .utils.emails.auth_security import send_email_otp
from .utils.machine.get_data_machine import get_client_info
from .utils.location.get_location_info import get_location_info



# LOGIN ACCESS SERIALIZER
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

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials.",
                code='authentication_failed'
            )

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        data['user'] = user
        return data

    def to_representation(self, instance):
        return {
            'id': instance['user'].id,
            'email': instance['user'].email,
            'first_name': instance['user'].first_name,
            'last_name': instance['user'].last_name,
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
        """
        Override is_valid to modify error format.
        """
        is_valid = super(UserRegisterSerializer, self).is_valid(raise_exception=False)
        
        # If validation errors are found and it's a non_field_error
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
        # Here we pop 'passconf' because it's not a field in our model.
        validated_data.pop('passconf')

        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail', max_length=254)

    def validate_email(self, value):
        user = CustomUser.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError('E-mail não encontrado')

        otp_code = str(random.randint(100000, 999999))
        token = base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8')

        #ip_address = requests.get('https://api.ipify.org').text
        ip_address = self.context['request'].META.get('REMOTE_ADDR')

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
        request = self.context.get('request')
        machine_info = get_client_info(request)  
        location_info = get_location_info(ip_address)
        #send_email_otp(user, otp_code, machine_info, location_info)
        print(user, otp_code, machine_info, location_info)
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