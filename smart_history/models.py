from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from security.models import CustomUser
from employee_management.models import EmployeeInfo
from smartmecanico.models.address_model import Address, CustomUser
from smartmecanico.models.vehicle_model import Vehicle
from smartmecanico.models.services_model import Service
from smartmecanico.models.appointment_model import Appointment

class History(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    date = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=10)
    data_snapshot = models.JSONField(help_text="Snapshot of the object's data at this point in time")

    class Meta:
        verbose_name = "Histórico"
        verbose_name_plural = "Históricos"
        ordering = ['-date']

    def __str__(self):
        return f"{self.event_type} on {self.date}"

class UserHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image_path = models.TextField(null=True, blank=True) 
    bio = models.TextField(max_length=500, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    failed_login_attempts = models.PositiveIntegerField()
    last_failed_login = models.DateTimeField(null=True, blank=True)
    history_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de Usuário"
        verbose_name_plural = "Históricos de Usuários"
        ordering = ['-history_date']

    def __str__(self):
        return f"History for user: {self.user.email} at {self.history_date}"


    class Meta:
        verbose_name = "Histórico de Usuário"
        verbose_name_plural = "Históricos de Usuários"
        ordering = ['-user']

    def __str__(self):
        return f"History for user: {self.user.username}"

class ServiceHistory(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Histórico de Serviço"
        verbose_name_plural = "Históricos de Serviços"
        ordering = ['-service']

    def __str__(self):
        return f"History for service: {self.service.name}"

class AppointmentHistory(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')])
    reason = models.TextField(null=True, blank=True) 

    class Meta:
        verbose_name = "Histórico de Agendamento"
        verbose_name_plural = "Históricos de Agendamentos"
        ordering = ['-appointment']

    def __str__(self):
        return f"History for appointment: {self.appointment.protocol}"

class AppointmentCancellationHistory(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, related_name="cancellation_history")
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="cancelled_appointments")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    cancellation_reason = models.TextField(help_text="Justificativa para o cancelamento")
    cancellation_date = models.DateTimeField(auto_now_add=True)
    data_snapshot = models.JSONField(help_text="Snapshot of the appointment's data at the time of cancellation")
    
    class Meta:
        verbose_name = "Histórico de Cancelamento de Agendamento"
        verbose_name_plural = "Históricos de Cancelamentos de Agendamentos"
        ordering = ['-cancellation_date']

    def __str__(self):
        return f"Cancelamento para {self.appointment} em {self.cancellation_date}"
