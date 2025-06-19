from django.contrib import admin
from django.core.mail import send_mail
from django.contrib import messages
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company_email', 'pvt_email', 'mobile')
    actions = ['send_verification_email']

    def send_verification_email(self, request, queryset):
        for employee in queryset:
            subject = "Employee Verification"
            message = f"""Hello {employee.first_name} {employee.last_name},

This is your verification email.

Employee ID: {employee.id}
Private Email: {employee.pvt_email}

Please verify and keep this information safe.

Thank you."""
            try:
                send_mail(subject, message, None, [employee.pvt_email])
                self.message_user(request, f"Email sent to {employee.pvt_email}.", messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f"Failed to send email to {employee.pvt_email}: {e}", messages.ERROR)

    send_verification_email.short_description = "Send Verification Email to Selected Employees"
