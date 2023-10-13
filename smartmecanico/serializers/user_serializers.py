from rest_framework import serializers
from security.models import CustomUser
import string
import random

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

class CustomUserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'image', 'birthday', 'phone_number', 'is_active', 'is_staff', 'is_superuser')
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = generate_random_password()
        email = validated_data.pop('email')
        user = CustomUser.objects.create_user(email=email, password=password)
        user.first_name = validated_data.get('first_name', '')
        user.last_name = validated_data.get('last_name', '')
        user.phone_number = validated_data.get('phone_number', '')
        user.birthday = validated_data.get('birthday', None)
        user.save()
        return user




class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'image', 'birthday', 'phone_number', 'is_active', 'is_staff', 'is_superuser')
        read_only_fields = ('id',)
