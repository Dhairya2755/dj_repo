from django.shortcuts import render, redirect, get_object_or_404
from .models import UserRegistration, Employee, EmployeeProfile

import re
from django.core.mail import send_mail

# Validate strong password
def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"\d", password):
        return "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

#  Register verification via email
def verification(request):
    if request.method == "POST":
        email = request.POST.get("email")
        employee = Employee.objects.filter(pvt_email=email).first()
        if employee:
            subject = "Welcome to the Company – Your Employee Credentials"
            message = f"""
Dear {employee.first_name} {employee.last_name},

Welcome to the team! Your account has been created.

──────────────
Employee ID: {employee.employee_id}
Password: {employee.password}
──────────────

Please log in at the portal. Change your password after login.

Best regards,  
ADMIN Team  
Dhairya Gandhi
"""
            try:
                send_mail(subject, message, None, [employee.pvt_email])
                return redirect('emplogin')
            except Exception as e:
                return render(request, 'dashboard/verification.html', {"error": f"Email error: {e}"})
        else:
            return render(request, 'dashboard/verification.html', {"error": "Email not registered."})

    return render(request, 'dashboard/verification.html')

#  Employee login
def employeelogin(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        employee = Employee.objects.filter(employee_id=employee_id, password=password).first()
        if employee:
            # Store in session
            request.session['employee_id'] = employee.employee_id
            request.session['employee_name'] = f"{employee.first_name} {employee.last_name}"
            return redirect('index_inner')
        else:
            return render(request, 'dashboard/emplogin.html', {'error': 'Invalid credentials'})
    return render(request, 'dashboard/emplogin.html')

#  Dashboard home page
def index_inner(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('emplogin')

    employee = get_object_or_404(Employee, employee_id=employee_id)
    return render(request, 'dashboard/index_inner.html', {'employee': employee})

#  Logout
def logout(request):
    request.session.flush()  # Clears session
    return redirect('emplogin')

#  Edit profile view
# def edit_profile(request):
#     employee_id = request.session.get('employee_id')
#     if not employee_id:
#         return redirect('emplogin')

#     employee = get_object_or_404(Employee, employee_id=employee_id)

#     if request.method == 'POST':
#         form = EmployeeEditForm(request.POST, instance=employee)
#         if form.is_valid():
#             form.save()
#             return redirect('index_inner')
#     else:
#         form = EmployeeEditForm(instance=employee)

#     return render(request, 'dashboard/edit_profile.html', {'form': form, 'employee': employee})

# My salary slips view (static mock)
def profile_view(request):
    employee = Employee.objects.first()  # For demo; you should use session ID
    salary_slips = [
        {"month": "May", "year": 2025, "download_url": "#"},
        {"month": "Apr", "year": 2025, "download_url": "#"},
        {"month": "Mar", "year": 2025, "download_url": "#"},
        {"month": "Feb", "year": 2025, "download_url": "#"},
    ]
    return render(request, 'dashboard/profile.html', {'employee': employee, 'salary_slips': salary_slips})

# update info
def edit_profile(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('emplogin')

        # employee = get_object_or_404(Employee, employee_id=employee_id)
        # return render(request, 'dashboard/edit_profile.html', {'employee': employee})
    return render(request, 'dashboard/edit_profile.html')
