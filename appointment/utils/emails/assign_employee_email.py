from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_mechanic_details_to_client(appointment, new_employee):
    recipient_email = appointment.user.email
    subject = 'Detalhes do Mecânico Designado | Smart Mecânico'
    template_name = 'emails/client_employee_details.html'

    # Obtendo detalhes adicionais do novo empregado para passar ao contexto
    employee_details = {
        "first_name": new_employee.first_name,
        "last_name": new_employee.last_name,
        "photo_url": getattr(new_employee, 'photo.url', None),  # A URL da foto, se disponível
        # Adicione aqui qualquer outro detalhe que você deseja enviar
    }

    context = {
        'appointment': appointment,
        'new_employee': new_employee,
        'employee_details': employee_details,  # Passando os detalhes do empregado ao contexto
    }

    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [recipient_email], html_message=html_message)


def send_service_order_to_employee(appointment):
    recipient_email = appointment.employee.user.email  # Corrigindo para ser apenas o email do empregado
    subject = 'Ordem de Serviço | Smart Mecânico'
    template_name = 'emails/employee_service_order.html'

    context = {
        'appointment': appointment,
        'client': appointment.user,
        'address': appointment.address,
        'vehicle': appointment.vehicle
    }

    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [recipient_email], html_message=html_message)
