from rest_framework import viewsets, permissions
from django.shortcuts import redirect, render
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentDetailSerializer
from .forms import CustomAppointmentForm


class IsAppointmentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class AppointmentModelViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AppointmentDetailSerializer
        return AppointmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAppointmentOwner]

        return [permission() for permission in permission_classes]



def custom_add_appointment(request):
    if request.method == 'POST':
        form = CustomAppointmentForm(request.POST)
        if form.is_valid():
            # Processar o formulário e salvar o objeto
            appointment = form.save()
            return redirect('admin:appointment_appointment_change', appointment.id)
    else:
        form = CustomAppointmentForm()

    return render(request, 'admin/appointment/custom_add_appointment.html', {'form': form})
