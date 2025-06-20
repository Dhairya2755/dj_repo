# models.py
from django.db import models
from django.utils.crypto import get_random_string
import uuid

class BaseClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserRegistration(BaseClass):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.name

class Employee(BaseClass):
    employee_id = models.CharField(max_length=10, unique=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_email = models.EmailField(unique=True)
    pvt_email = models.EmailField(unique=True)
    mobile = models.IntegerField()
    password = models.CharField(max_length=8, blank=True)
    doj = models.DateField()

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
