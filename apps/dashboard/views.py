from django.shortcuts import render,redirect
from .models import UserRegistration
import re
from django.core.mail import send_mail
from .models import Employee
from .models import EmployeeProfile

# Create your views here.

# def index_inner(request):
#     return render(request,'dashboard/index_inner.html')

# def index_outer(request):
#     return render(request,'index_outer.html')
def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"\d", password):
        return "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

# Register View
# def register(request):
#     if request.method == "POST":
#         fullname = request.POST.get("fullname")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")

#         error = validate_password(password)
#         if error:
#             return render(request, 'dashboard/register.html', {"error": error})

#         if password != confirm_password:
#             return render(request, 'dashboard/register.html', {"error": "Passwords do not match."})

#         UserRegistration.objects.create(
#             fullname=fullname,
#             email=email,
#             password=password
#         )
#         return redirect('login')  # Go to login after registration

#     return render(request, 'dashboard/register.html')

# Login View
# def login_view(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Simple database check
#         user = UserRegistration.objects.filter(email=email, password=password).first()
#         if user:
#             return redirect('index_inner')
#         else:
#             return render(request, 'dashboard/login.html', {'error': 'Invalid credentials'})

#     return render(request, 'dashboard/login.html')

# Dashboard
# def index_inner(request):
#     return render(request, 'dashboard/index_inner.html')

# #logout
# def logout(request):
#     # del request.session['']
#     #return redirect(request,'dashboard/register.html')
#     #return redirect(request,'dashboard/login.html')
#     return redirect ('login')

# def employeelogin(request):
#     return render(request, 'dashboard/emplogin.html')

# def verification(request):
#     return render(request, 'dashboard/register.html')



def verification(request):
    if request.method == "POST":
        email = request.POST.get("email")
        employee = Employee.objects.filter(pvt_email=email).first()
        if employee:
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
🔁 It is **strongly recommended** that you change your password after first login to ensure your account security.

📌 If you face any issues accessing the portal or if you have any questions, feel free to reach out to the IT department at gandhidhairya510@gmail.com.

Once again, welcome aboard! We are thrilled to have you with us and look forward to your valuable contributions.

Best regards,  
ADMIN Team  
  Dhairya Gandhi
"""
            try:
                send_mail(subject, message, None, [employee.pvt_email])
                return redirect('emplogin')
            except Exception as e:
                return render(request, 'dashboard/verification.html', {"error": f"Failed to send email: {e}"})
        else:
            return render(request, 'dashboard/verification.html', {"error": "Email not registered."})

    return render(request, 'dashboard/verification.html')



def employeelogin(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        employee = Employee.objects.filter(employee_id=employee_id, password=password).first()
        if employee:
            return redirect('index_inner')
        else:
            return render(request, 'dashboard/emplogin.html', {'error': 'Invalid credentials'})
    return render(request, 'dashboard/emplogin.html')


def index_inner(request):
    return render(request, 'dashboard/index_inner.html')

def logout(request):
    return redirect('emplogin')



def dashboard_view(request):
    profile = EmployeeProfile.objects.get(user=request.user)
    return render(request, 'index_inner.html', {'profile': profile})