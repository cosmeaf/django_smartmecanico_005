from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_appointment_confirmation_email(action, instance, original_instance=None):
    recipient_email = instance.user.email
    subject = ''
    context = {'appointment': instance}

    # Escolhendo o template de email correto para cada ação
    template_name = ''

    if action == 'creation':
        subject = 'Serviço de Agendamento | Smart Mecânico'
        template_name = 'emails/appointment_creation_email.html'

    elif action == 'update':
        subject = 'Atualizaçao de Agendamento | Smart Mecânico'
        template_name = 'emails/appointment_update_email.html'
        if instance.employee:
            context['employee'] = instance.employee

    elif action == 'deletion':
        subject = 'Cancelamento de Serviço Agendado | Smart Mecânico'
        template_name = 'emails/appointment_deletion_email.html'
        # Você pode adicionar mais contextos aqui, se necessário, por exemplo:
        # context['reason'] = 'Razão para o cancelamento'

    # Renderizando o e-mail usando o template e o contexto
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)

    # Enviando o e-mail
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, 
              [recipient_email], html_message=html_message)