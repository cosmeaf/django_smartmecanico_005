from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from .models import Appointment
from .utils.emails.assign_employee_email import send_mechanic_details_to_client, send_service_order_to_employee
from .utils.emails.appointment_email import send_appointment_confirmation_email


@receiver(pre_save, sender=Appointment)
def appointment_pre_save(sender, instance, **kwargs):
    try:
        instance._original_instance = Appointment.objects.get(pk=instance.pk)
    except Appointment.DoesNotExist:
        # Isso será um novo objeto, então não há instância original
        pass


@receiver(post_save, sender=Appointment)
def appointment_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"Agendamento Criado {instance}")
        send_appointment_confirmation_email('creation', instance)
    else:
        original_instance = getattr(instance, '_original_instance', None)

        if original_instance:
            if instance.user != original_instance.user or \
               instance.address != original_instance.address or \
               instance.vehicle != original_instance.vehicle or \
               instance.service != original_instance.service or \
               instance.hour != original_instance.hour or \
               instance.day != original_instance.day:
                print(f"ATUALIZAÇÃO POST_SAVE {instance}, {original_instance}")
                send_appointment_confirmation_email('update', instance, original_instance)

            if instance.employee != original_instance.employee:
                if instance.employee:  # Checando se um mecânico foi atribuído
                    employee_details = f"ID: {instance.employee.id}, Nome: {instance.employee.first_name} {instance.employee.last_name}"
                    if hasattr(instance.employee, 'photo'):
                        employee_details += f", Foto: {instance.employee.photo.url}"

                    print(f"Designação de Mecânico {instance}, Mecânico: {employee_details}")
                    send_mechanic_details_to_client(instance, instance.employee)
                    send_service_order_to_employee(instance)
                else:  # Se não há mecânico atribuído
                    print(f"Designação de Mecânico {instance}, Sem mecânico atribuído")
                    # Envie um email aqui informando que não há mais um mecânico atribuído


@receiver(pre_delete, sender=Appointment)
def appointment_pre_delete(sender, instance, **kwargs):
    print(f"Exclusão de Agendamento {instance}")
    send_appointment_confirmation_email('deletion', instance)