from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .utils import generate_salary_pdf
from datetime import datetime
from .forms import *

import re
import uuid
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
Tech Nova Desk
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

    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == 'POST':
        # Defensive check
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not first_name or not last_name:
            return render(request, 'dashboard/edit_profile.html', {
                'employee': employee,
                'error': 'First and Last name are required.'
            })

        employee.first_name = first_name
        employee.last_name = last_name
        employee.company_email = request.POST.get('company_email', '').strip()
        employee.pvt_email = request.POST.get('pvt_email', '').strip()
        employee.mobile = request.POST.get('mobile', '').strip()
        employee.designation = request.POST.get('designation', '').strip()
        employee.department = request.POST.get('department', '').strip()
        employee.location = request.POST.get('location', '').strip()
        employee.save()

        return redirect('index_inner')

    return render(request, 'dashboard/edit_profile.html', {'employee': employee})

#general information
def generalinfo(request):
    employee_id_ = request.session.get('employee_id')
    emp= Employee.objects.get(employee_id= employee_id_)
    context ={
        'employee':emp
    }
    
    return render(request, 'dashboard/generalinfo.html',context)

#qualification

def qualification_form(request):
    employee = Employee.objects.filter(employee_id='emp012').first()  # Use session or login in real case

    if request.method == 'POST':
        QualificationDetail.objects.create(
            employee=employee,
            qualification_type=request.POST.get('qualification_type'),
            course_name=request.POST.get('course_name'),
            specialization=request.POST.get('specialization'),
            course_type=request.POST.get('course_type'),
            school_college=request.POST.get('school_college'),
            board_university=request.POST.get('board_university'),
            percentage=request.POST.get('percentage'),
            passing_year=request.POST.get('passing_year'),
            document=request.FILES.get('document')
        )
        return redirect('index_inner')

    return render(request, 'dashboard/qualification_form.html', {'employee': employee})


#induction feedback 
def induction(request):
    questions = {
    1: "I felt welcomed on joining.",
    2: "I had an energetic beginning and my Induction Program was very engaging.",
    3: "I felt that I was importing during my Induction Period.",
    4: "My workstation was up and running on the first day of the joining.",
    5: "I got all the resources timely viz Laptop, datacard, mobile etc, that I need to start functioning.",
    6: "I felt confident about the Knowledge of the Company gained during Induction period.",
    7: "My Departmental Induction was conducted effectively.",
    8: "I know my Job Description and my reporting manager have explained my role to me.",
    9: "I started feeling comfortable in the company because of the Induction Program.",
    10: "I feel connected with the company & a part of the team because of induction program."
}
    
    return render(request, 'dashboard/induction-feedback.html', {"questions": questions})

#mediclaim details
from django.shortcuts import render, redirect
from .models import Employee, FamilyMember
from datetime import date

def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def family_info(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('emplogin')

    employee = Employee.objects.get(employee_id=employee_id)
    family_members = FamilyMember.objects.filter(employee=employee)

    if request.method == 'POST':
        dob = request.POST.get('dob')
        name = request.POST.get('name')
        age = calculate_age(date.fromisoformat(dob))

        FamilyMember.objects.create(
            employee=employee,
            name=name,
            dob=dob,
            age=age,
            relation=request.POST.get('relation'),
            gender=request.POST.get('gender'),
            residing_with=request.POST.get('residing_with'),
            mobile=request.POST.get('mobile'),
            differently_abled=request.POST.get('differently_abled'),
            nominee=request.POST.get('nominee'),
        )
        return redirect('family_info')

    return render(request, 'dashboard/family_info.html', {
        'employee': employee,
        'family_members': family_members
    })


#general information update
def updategeneral(request):
    employee_id_ = request.session.get('employee_id')
    empl = Employee.objects.get(employee_id = employee_id_)
    context1 = {
        'employee': empl
    }

    return render(request, 'dashboard/geninfoupdate.html',context1)

#policy circular
def policy_and_circular(request):
    return render(request, 'dashboard/policy_and_circular.html')

# def generate_salary_slip(request):
#     employee_id_ = request.session['employee_id']

#     get_employee = get_object_or_404(Employee, id=employee_id_)
#     get_employee_salary_detail = get_object_or_404(EmployeeSalary, employee_id=employee_id_)
#     print(get_employee, get_employee_salary_detail)
#     return redirect('index_inner')


#salary slips
# def generate_salary_view(request):
#     employee_id_ = request.session.get('employee_id')
#     if not employee_id_:
#         return redirect('emplogin')
#     print(type(employee_id_))
#     employee = Employee.objects.get(id=uuid(employee_id_))
#     emp_s=EmployeeSalary.objects.get(id=uuid(employee_id_))
#     HRA=emp_s.salary*50/100
#     current_year = datetime.now().year
#     salary={
#         'name':employee.first_name+employee.last_name,
#         'email':employee.pvt_email,
#         'mob':employee.mobile,
#         'Salary':emp_s.salary,
#         'HRA':HRA,
    # }
    # Autogenerate last 12 months
    # for i in range(12):
    #     month = (datetime.now().month - i - 1) % 12 + 1
    #     year = current_year if datetime.now().month - i > 0 else current_year - 1

    #     slip, {
    #         employee=emp)loyee, month=month, year=year
    #     }
    # #     if created or not slip.pdf:
    #         generate_salary_pdf(slip)

    # slips = EmployeeSalary.objects.filter(employee=employee).order_by('-year', '-month')\

  #  return render(request, 'dashboard/salary_slips.html',salary)

#loan
def loan_history_view(request):
    loans = Loan.objects.select_related('employee').all()
    form = LoanForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('loan_history')

    return render(request, 'dashboard/loan_history.html', {'form': form, 'loans': loans})



