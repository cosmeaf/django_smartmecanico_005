# utils/emails/auth_account.py

from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def register_account(user):
    subject = 'Bem-vindo ao Smart Mecânico!'
    template_name = 'emails/register_account.html'
    
    context = {
        'first_name': user.first_name,
    }

    try:
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)

        send_mail(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_content)
        
        logger.info('E-mail enviado com sucesso para: %s', user.email)
        return True

    except BadHeaderError:
        logger.error(f"Erro ao enviar email de criação para {user.email}: Header inválido encontrado.")
        return False
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {user.email}: {e}")
        return False
