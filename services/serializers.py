from rest_framework import serializers
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Service, HourService


class HourServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourService
        fields = ['id', 'hour']

    def validate_hour(self, value):
        try:
            datetime.strptime(value, '%H:%M')
        except ValueError:
            raise ValidationError("A hora fornecida não está no formato correto (HH:MM).")
        return value


class ServiceSerializer(serializers.ModelSerializer):
    hour_service = HourServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'image', 'name', 'description', 'hour_service']
    
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("O nome do serviço deve conter pelo menos 3 caracteres.")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("A descrição deve conter pelo menos 10 caracteres.")
        return value
