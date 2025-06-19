from django.db import models
import uuid
# Create your models here.



class BaseClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserRegistration(BaseClass):
    name = models.CharField(max_length=100,blank=False,null=False)
    email = models.EmailField(unique=True,blank=False,null=False)
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.name
    
class Employee(BaseClass):
    first_name = models.CharField(max_length=255,blank=False,null=False)
    last_name = models.CharField(max_length=255,blank=False,null=False)
    company_email = models.EmailField(unique=True,blank=False,null=False)
    pvt_email = models.EmailField(unique=True,blank=False,null=False)
    mobile = models.IntegerField(blank=False,null=False)
    doj = models.DateField(null=False)


class EmployeePersonalInfo(BaseClass):
    gender = models.CharField(max_length=255,null=False,blank=False)
    dob = models.DateField(null=False)
    pfp = models.ImageField(null=False,blank=False)

    