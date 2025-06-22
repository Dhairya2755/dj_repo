from django.db import models
from django.utils.crypto import get_random_string
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


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
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='employee_photos/', default='default.jpg')

    def __str__(self):
        return self.user.get_full_name()
    


@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(user=instance)



class InductionFeedback(models.Model):
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



class QualificationDetail(models.Model):
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
