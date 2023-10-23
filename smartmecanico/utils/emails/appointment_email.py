from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_email(subject, template_name, appointment):
    context = {
        'appointment': appointment,
    }

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [appointment.user.email]
    html_message = render_to_string(template_name, context)
    company_email = "contato@smartmecanico.com.br"
    
    email = EmailMessage(
        subject,
        html_message,
        from_email,
        recipient_list,
        bcc=[company_email]
    )
    email.content_subtype = "html"
    email.send()

def send_appointment_creation_email(appointment):
    send_email('Smart Mecânico | Confirmação de agendamento', 'emails/appointment_creation_confirmation.html', appointment)

def send_appointment_update_email(appointment):
    send_email('Smart Mecânico | Atualização de agendamento', 'emails/appointment_update_confirmation.html', appointment)

def send_appointment_deletion_email(appointment):
    send_email('Smart Mecânico | Notificação de cancelamento', 'emails/appointment_deletion_confirmation.html', appointment)
