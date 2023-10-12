# security/utils/emails/auth_security.py
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_created_account_email(user, ip_address=None, machine_info=None, location_info=None):
    try:
        subject = 'Smart Mecânico - Criaçao de Conta'
        context = {
            'user': user,
            'ip_address': ip_address,
            'machine_info': machine_info,
            'location_info': location_info
        }
        html_message = render_to_string('emails/created_account.html', context)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(
            subject,
            message=None,
            html_message=html_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email enviado com sucesso para: {user.email}")
    except Exception as e:
        logger.error(f"Erro ao enviar email para {user.email}: {str(e)}")



def send_email_otp(user, otp_code, device_info, location_info):
    context = {
        'otp_code': otp_code,
        'user': user,
        'device_info': device_info,
        'location_info': location_info,
    }
    subject = 'Seu código de verificação'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    html_message = render_to_string('emails/otp_code.html', context)
    send_mail(
        subject,
        message=None,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )


def send_password_changed(user, device_info):
    """
    Envia um e-mail ao usuário notificando sobre a alteração da senha.
    """
    try:
        context = {
            'user': user,
            'ip_address': device_info['ip_address'],
            'browser': device_info['browser'],
            'device': device_info['device'],
            'os_name': device_info['os_name'],
            'os_version': device_info['os_version'],
        }

        subject = 'Alteração de senha'
        html_message = render_to_string('emails/password_changed.html', context)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(
            subject,
            message=None,
            html_message=html_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        logger.info(f"E-mail de notificação de alteração de senha enviado para {user.email}.")

    except Exception as e:
        logger.error(f"Erro ao enviar e-mail de notificação de alteração de senha: {str(e)}")



