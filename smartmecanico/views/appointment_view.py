from rest_framework import status, serializers, viewsets, permissions
from security.models import CustomUser
from smartmecanico.models.appointment_model import Appointment
from smartmecanico.serializers.appointment_serializers import AppointmentSerializer, AppointmentDetailSerializer

class IsAppointmentOwner(permissions.BasePermission):
    """ 
    Permissão personalizada que permite superusuários verem e alterarem qualquer agendamento,
    enquanto usuários normais só podem ver e alterar seus próprios agendamentos.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user

class AppointmentModelViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Se o usuário logado é superusuário e o campo 'user' foi especificado no payload
        if self.request.user.is_staff and 'user' in serializer.validated_data:
            user = serializer.validated_data['user']
            serializer.save(user=user)
        # Se não, o agendamento é associado ao usuário logado
        else:
            serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAppointmentOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'list']:
            return AppointmentSerializer
        return AppointmentDetailSerializer
