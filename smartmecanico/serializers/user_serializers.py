from rest_framework import serializers
from security.models import CustomUser

# USER SERIALIZER
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'image', 'birthday', 'phone_number', 'is_active', 'is_staff', 'is_superuser',)
        read_only_fields = ('id',)

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'image', 'birthday', 'phone_number', 'is_active', 'is_staff', 'is_superuser',)
        read_only_fields = ('id',)
