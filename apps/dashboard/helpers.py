# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Employee

@receiver(post_save, sender=Employee)
def send_employee_credentials(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome! Your Employee Login Credentials"
        message = f"""Hello {instance.first_name} {instance.last_name},

Your account has been created.

Employee ID: {instance.employee_id}
Password: {instance.password}

Use your credentials to log in.

Regards,
Admin Team
"""
        send_mail(subject, message, None, [instance.company_email])
