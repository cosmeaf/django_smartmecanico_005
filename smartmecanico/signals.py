from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from smartmecanico.models.appointment_model import Appointment
from smartmecanico.utils.emails.appointment_email import (send_appointment_creation_email, 
send_appointment_update_email, send_appointment_deletion_email)
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Appointment)
def appointment_post_save(sender, instance, created, **kwargs):
    try:
        if created:
            send_appointment_creation_email(instance)
            logger.info('Creation email sent for %s', instance)
        else:
            send_appointment_update_email(instance)
            logger.info('Update email sent for %s', instance)
    except Exception as e:
        logger.error(f"Erro ao enviar email para {instance.user.email}: {str(e)}")
    finally:
        logger.info("Processamento do sinal de agendamento concluído.")


@receiver(pre_delete, sender=Appointment)
def appointment_pre_delete(sender, instance, **kwargs):
    try:
        send_appointment_deletion_email(instance)
        logger.info('Deletion email sent for %s', instance)
    except Exception as e:
        logger.error(f"Erro ao enviar email de deleção para {instance.user.email}: {str(e)}")
    finally:
        logger.info("Processamento do sinal de deleção de agendamento concluído.")
