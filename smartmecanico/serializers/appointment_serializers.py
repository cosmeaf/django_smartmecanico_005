from rest_framework import serializers
from smartmecanico.models.appointment_model import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'user', 'address', 'vehicle', 'service', 'hour', 'day', 'protocol', 'employee']
        read_only_fields = ('id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['day'] = instance.day.strftime('%d/%m/%Y')
        return representation

class AppointmentDetailSerializer(AppointmentSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'user', 'address', 'vehicle', 'service', 'hour', 'day', 'protocol', 'employee', 'created_at', 'updated_at', 'deleted_at']
