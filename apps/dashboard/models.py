from django.db import models
from django.utils.crypto import get_random_string
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User 
import random
from datetime import date




# Abstract base class with UUID + timestamps
class BaseClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# User Registration for manual/extra users
class UserRegistration(BaseClass):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.name

# Main Employee Model
class Employee(BaseClass):
    employee_id = models.CharField(max_length=10, unique=True, blank=True)
    first_name = models.CharField(max_length=255,null=False,blank=False)
    last_name = models.CharField(max_length=255,null=False,blank=False)
    company_email = models.EmailField(unique=True,null=False,blank=False)
    pvt_email = models.EmailField(unique=True,null=False,blank=False)
    mobile = models.CharField(max_length=15,null=False,blank=False)
    password = models.CharField(max_length=8, blank=True,null=False)

    doj = models.DateField(verbose_name="Date of Joining",null=False,blank=False)
    dob = models.DateField(verbose_name="Date of Birth", default="2000-01-01")


    # Optional details
    location = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    manager = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='employee_photos/', default='default.jpg')

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_emp = Employee.objects.order_by('-created_at').first()
            if last_emp and last_emp.employee_id:
                last_num = int(last_emp.employee_id.replace('emp', ''))
                self.employee_id = f"emp{last_num+1:03d}"
            else:
                self.employee_id = "emp001"

        if not self.password:
            self.password = get_random_string(length=8)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Employee Profile photo (linked to Django auth user)
class EmployeeProfile(BaseClass):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='employee_photos/', default='default.jpg')

    def __str__(self):
        return self.user.get_full_name()
    


@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(user=instance)



class InductionFeedback(BaseClass):
    employee_id = models.CharField(max_length=10, unique=True, blank=True)
    first_name = models.CharField(max_length=255,null=False,blank=False)
    
    q1 = models.CharField(max_length=5)
    q2 = models.CharField(max_length=5)
    q3 = models.CharField(max_length=5)
    q4 = models.CharField(max_length=5)
    q5 = models.CharField(max_length=5)
    q6 = models.CharField(max_length=5)
    q7 = models.CharField(max_length=5)
    q8 = models.CharField(max_length=5)
    q9 = models.CharField(max_length=5)
    q10 = models.CharField(max_length=5)
    
    remark = models.TextField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} {self.first_name} "



class QualificationDetail(BaseClass):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    qualification_type = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    course_type = models.CharField(max_length=50)
    school_college = models.CharField(max_length=150)
    board_university = models.CharField(max_length=150)
    percentage = models.CharField(max_length=20)
    passing_year = models.CharField(max_length=10)
    document = models.FileField(upload_to='qualifications/', blank=True, null=True)

    def __str__(self):
        return f"{self.employee.employee_id} - {self.course_name}"


class FamilyMember(BaseClass):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.PositiveIntegerField()
    relation = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    residing_with = models.CharField(max_length=10)  # Yes/No
    mobile = models.CharField(max_length=15)
    differently_abled = models.CharField(max_length=10)  # Yes/No
    nominee = models.CharField(max_length=10)  # Yes/No
    disabled = models.BooleanField(default=False)
    date_of_demise = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.employee.employee_id})"
    
# import random

# def random_salary():
#     return random.randint(1000,20000)


# class EmployeeSalary(BaseClass):
#     employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     amount = models.DecimalField(decimal_places=2, default=25000+random_salary(), max_digits=10)

   
class Loan(BaseClass):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    loan_no = models.CharField(max_length=50)
    principal_amount_type = models.CharField(max_length=50)
    loan_type = models.CharField(max_length=50)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    applied_on = models.DateField()
    wef_from = models.DateField(verbose_name="Loan WEF From")
    deduct_from = models.DateField(verbose_name="Loan Deduct From")
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2)
    tenure_months = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"{self.loan_no} - {self.employee.first_name} {self.employee.last_name}"
    
class DocumentAcceptance(BaseClass):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"{self.employee.first_name} - {self.document_name} ({self.status})"


class InvestmentProofStatus(BaseClass):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    section = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    policy_no = models.CharField(max_length=100)
    payment_date = models.DateField()
    relation_with_beneficiary = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_to_be_received = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.first_name} - {self.section}"


class HRARentProofStatus(BaseClass):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    city = models.CharField(max_length=100)
    metro = models.CharField(max_length=10)  # Yes/No
    landlord_pan = models.CharField(max_length=50)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_to_be_received = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.first_name} - Rent Proof"

class Claim(BaseClass):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    ref_no = models.CharField(max_length=100)
    claim_code = models.CharField(max_length=50)
    claim_type = models.CharField(max_length=50)
    claim_date = models.DateField()
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ref_no} - {self.employee.first_name}"

class ClaimStatus(BaseClass):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    ref_no = models.CharField(max_length=100)
    description = models.TextField()
    bill_no = models.CharField(max_length=100)
    bill_date = models.DateField()
    claimed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rejected_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ref_no} - {self.employee.first_name}"


class Salary(BaseClass):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=35000.00)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=10500.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=2500.00)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.net_salary = self.basic_salary + self.hra - self.tax
        super().save(*args, **kwargs)


class SalarySlip(BaseClass):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)  # e.g., 'June'
    year = models.IntegerField()
    pdf_file = models.FileField(upload_to='salary_slips/')

    class Meta:
        unique_together = ('employee', 'month', 'year')

    def __str__(self):
        return f"{self.employee.first_name} - {self.month} {self.year}"
