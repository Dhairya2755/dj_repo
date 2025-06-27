from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .utils import generate_salary_pdf
from datetime import datetime  , timedelta 
from .forms import *
import re
import uuid
from django.core.mail import send_mail
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.core.files.base import ContentFile
from io import BytesIO
from django.utils import timezone


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
        request.session['start_time'] = timezone.now().timestamp()
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
    print("*****-1")
    employee_id = request.session.get('employee_id')
    
    if not employee_id:
        print("*****-2")
        return redirect('emplogin')

    employee = get_object_or_404(Employee, employee_id=employee_id)
    print("*****-3")

    total_employees = Employee.objects.count()
    print("*****-4")
    print(total_employees)
    salary_slips = SalarySlip.objects.filter(employee=employee).order_by('-year', '-month')[:3]
    family_members = FamilyMember.objects.filter(employee=employee)

    return render(request, 'dashboard/index_inner.html', {
        'employee': employee,
        'total_employees': total_employees,
        'salary_slips': salary_slips,
        'family_members': family_members
    })


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
    employee_id = request.session.get('employee_id')
    employee = Employee.objects.filter(employee_id=employee_id).first()  # Use session or login in real case

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
    employee_id = request.session.get('employee_id')
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == 'POST':
        form = EmployeeGeneralInfoForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('generalinfo')  # or any page you like
    else:
        form = EmployeeGeneralInfoForm(instance=employee)

    return render(request, 'dashboard/geninfoupdate.html', {
        'form': form,
        'employee': employee  # to display non-editable fields
    })

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

#acceptance

def my_acceptance_view(request):
    documents = DocumentAcceptance.objects.select_related('employee').all()
    return render(request, 'dashboard/my_acceptance.html', {'documents': documents})

# proof status
def proof_status_view(request):
    inv_proofs = InvestmentProofStatus.objects.select_related('employee').all()
    hra_proofs = HRARentProofStatus.objects.select_related('employee').all()
    return render(request, 'dashboard/proof_status.html', {
        'inv_proofs': inv_proofs,
        'hra_proofs': hra_proofs,
    })


#claim status
def claims_view(request):
    form = ClaimForm(request.POST or None)
    claims = Claim.objects.select_related('employee').all()

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('claims_page')

    return render(request, 'dashboard/claims_page.html', {'form': form, 'claims': claims})

#claim status
def claim_status_view(request):
    statuses = ClaimStatus.objects.select_related('employee').all()
    return render(request, 'dashboard/claim_status.html', {'statuses': statuses})


#finalise salary
def salary_slip_list_view(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return render(request, 'salary_slips.html', {
            'slips': [],
            'salary': None,
            'error': 'No employee ID found in session.'
        })

    salary = Salary.objects.filter(employee__employee_id=employee_id).first()
    slips = SalarySlip.objects.filter(employee__employee_id=employee_id).order_by('-year', '-month')
    return render(request, 'dashboard/salary.html', {
        'slips': slips,
        'salary': salary,
        'error': None if salary else 'No salary assigned yet.'
        
    })
    
    #automatic salary 
  




def generate_salary_slip_pdf(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return HttpResponse("You are not logged in.")

    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return HttpResponse("Employee does not exist.")

    salary, created = Salary.objects.get_or_create(
        employee=employee,
        defaults={
            'basic_salary': 30000,
            'hra': 10000,
            'tax': 2000,
        }
    )
    if created:
        salary.save()

    
    month = datetime.now().strftime('%B')
    year = datetime.now().year

    if SalarySlip.objects.filter(employee=employee, month=month, year=year).exists():
        return HttpResponse("Salary slip already generated for this month.")

    context = {
        'employee': employee,
        'salary': salary,
        'month': month,
        'year': year,
    }

    template = get_template("dashboard/salary_slip_pdf.html")
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        slip = SalarySlip(
            employee=employee,
            month=month,
            year=year
        )
        slip.pdf_file.save(f"{employee.employee_id}_{month}_{year}.pdf", ContentFile(result.getvalue()))
        return HttpResponse("Salary slip generated successfully.")
    return HttpResponse("PDF generation failed.")

#bday countdown
def dashboard_highlights(request):
    today = date.today()
    upcoming = today + timedelta(days=7)  # show next 7 days

    # Birthdays this week (month/day match only)
    birthdays = Employee.objects.filter(
        date_of_birth__month__gte=today.month,
        date_of_birth__day__gte=today.day,
        date_of_birth__month__lte=upcoming.month,
        date_of_birth__day__lte=upcoming.day
    )
    return render(request, 'dashboard/index_inner.html', {
        'birthdays': birthdays,
    })


#bday reminder
def send_birthday_emails():
    today = date.today()
    celebrants = Employee.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )

    for emp in celebrants:
        send_mail(
            "Happy Birthday 🎂",
            f"Dear {Employee.first_name},\n\nWishing you a very happy birthday!\n\n— Team",
            None,
            [Employee.pvt_email],
        )
#leave mgmt
def leave_apply_view(request):
    employee_id = request.session.get('employee_id')
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        Leave.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        return redirect('leave_history')

    return render(request, 'dashboard/leave_apply.html', {'employee': employee})


def leave_history_view(request):
    employee_id = request.session.get('employee_id')
    employee = get_object_or_404(Employee, employee_id=employee_id)

    leaves = Leave.objects.filter(employee=employee).order_by('-start_date')
    return render(request, 'dashboard/leave_history.html', {'employee': employee, 'leaves': leaves})    


# #navbar
# def index_inner(request):
#     employee_id = request.session.get('employee_id')
#     if not employee_id:
#         return redirect('emplogin')
    
#     employee_count 
    
#     employee = get_object_or_404(Employee, employee_id=employee_id)
#     return render(request, 'dashboard/index_inner.html', {'employee': employee})



