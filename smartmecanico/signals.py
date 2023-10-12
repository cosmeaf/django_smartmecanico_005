from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from smartmecanico.models.appointment_model import Appointment
from smartmecanico.utils.emails.assign_employee_email import send_mechanic_details_to_client


@receiver(post_save, sender=Appointment)
def appointment_post_save(sender, instance, created, **kwargs):
    if created:
        send_appointment_confirmation_email('creation', instance)
    else:
        send_appointment_confirmation_email('update', instance)

@receiver(post_delete, sender=Appointment)
def appointment_post_delete(sender, instance, **kwargs):
    send_appointment_confirmation_email('deletion', instance)

@receiver(pre_save, sender=Appointment)
def check_employee_change(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    if not obj.employee == instance.employee:
        instance._employee_changed = True

@receiver(post_save, sender=Appointment)
def send_email_if_employee_changed(sender, instance, **kwargs):
    if hasattr(instance, '_employee_changed'):
        send_mechanic_details_to_client(instance, instance.employee)