from django.contrib import admin
from django.core.mail import send_mail
from django.contrib import messages
from .models import Employee
from .models import EmployeeProfile
from django.utils.html import format_html


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id', 'first_name', 'last_name','dob',
        'company_email','pvt_email','mobile','password', 'designation', 'department', 'doj','manager','location','photo'
    )
    search_fields = ('employee_id', 'first_name', 'last_name', 'company_email')
    readonly_fields = ('employee_id', 'password')
    actions = ['send_verification_email']

    def send_verification_email(self, request, queryset):
        for employee in queryset:
            subject = "Welcome to the Company – Your Employee Credentials"
            message = f"""
Dear {employee.first_name} {employee.last_name},

We are excited to welcome you to the team! Your employee account has been successfully created. Please find your login credentials and important onboarding information below.

────────────────────────────────────────────
Here are your credentials:

Employee ID: {employee.employee_id}
Password: {employee.password}

────────────────────────────────────────────

✅ Please log in to the employee portal using the above credentials.  
🔁 It is strongly recommended that you change your password after first login to ensure your account security.

📌 If you face any issues accessing the portal or have any questions, reach out to the IT department at gandhidhairya510@gmail.com.

Once again, welcome aboard! We are thrilled to have you with us and look forward to your valuable contributions.

Best regards,  
ADMIN Team  
Dhairya Gandhi
"""
            try:
                send_mail(subject, message, None, [employee.pvt_email])
                self.message_user(request, f"Email sent to {employee.pvt_email}.", messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f"Failed to send email: {e}", messages.ERROR)

    send_verification_email.short_description = "Send Manual Verification Email"



# @admin.register(EmployeeProfile)
# class EmployeeProfileAdmin(admin.ModelAdmin):
#     list_display = ('employees', 'profile_image')

#     def profile_image(self, obj):
#         if obj.photo:
#             return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.photo.url)
#         return "No image"

#     profile_image.short_description = 'Profile Picture'

