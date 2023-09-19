from rest_framework import serializers

from employee_management.models import EmployeeInfo
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    employee = serializers.PrimaryKeyRelatedField(queryset=EmployeeInfo.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Appointment
        exclude = ['created_at', 'updated_at', 'deleted_at']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': instance.user.username,
            'address': instance.address.cep,
            'service': instance.service.name,
            'vehicle': instance.vehicle.brand,
            'hour': instance.hour,
            'day': instance.day.strftime('%d/%m/%Y'),
            'protocol': instance.protocol,
            'employee': f"{instance.employee.first_name} {instance.employee.last_name}" if instance.employee else None,
        }


class AppointmentDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    address = serializers.StringRelatedField(source='address.cep')
    service = serializers.StringRelatedField(source='service.name')
    vehicle = serializers.StringRelatedField(source='vehicle.brand')
    employee = serializers.StringRelatedField(source='employee.first_name')

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'address', 'service', 'vehicle', 'hour', 'day', 'protocol', 'employee_first_name', 'employee_last_name']
