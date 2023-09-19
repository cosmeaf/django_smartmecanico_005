from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


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