from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import CustomUser, RecoverPassword
from .utils.emails.auth_security import send_created_account_email, send_email_otp, send_password_changed
from .utils.machine.get_data_machine import get_client_info
from .utils.location.get_location_info import get_location_info
import logging

logger = logging.getLogger(__name__)

user_created_signal = Signal()

@receiver(user_created_signal)
def process_user_creation(sender, instance, **kwargs):
    try:
        ip_address = kwargs.get('ip_address')
        machine_info = kwargs.get('machine_info')
        location_info = kwargs.get('location_info')
        logger.info(f"Conta criada com sucesso: {instance.email}, {ip_address}, {machine_info}, {location_info}")    
        send_created_account_email(user=instance, ip_address=ip_address, machine_info=machine_info, location_info=location_info)
    except Exception as e:
        logger.error(f"Erro ao processar a criação do usuário: {str(e)}")

@receiver(post_save, sender=RecoverPassword)
def process_recover_password(sender, instance, created, **kwargs):
    try:
        otp_code = instance.otp
        user = instance.user
        ip_address = instance.ip_address
        location_info = get_location_info(ip_address)

        if created:
            send_email_otp(user, otp_code, {}, location_info)
            logger.info(f"Nova solicitação de recuperação de senha para {user.email}.")
        else:
            # Isso implica que o registro foi atualizado
            if instance.is_used:
                device_info = {
                    'ip_address': instance.ip_address,
                    'browser': instance.browser,
                    'device': instance.device,
                    'os_name': instance.os_name,
                    'os_version': instance.os_version
                }

                # Chamar o método de envio de e-mail.
                send_password_changed(user, device_info)
                logger.info(f"Notificação de alteração de senha enviada para {user.email}.")

    except Exception as e:
        logger.error(f"Erro ao processar a solicitação de recuperação de senha: {str(e)}")
    finally:
        logger.info("Processamento do sinal de recuperação de senha concluído.")
