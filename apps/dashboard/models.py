from django.db import models

# Create your models here.


class BaseClass(models.Model):
    id = models.UUIDField(primary_key=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class CompnayRegistration(BaseClass):
    name = models.CharField(max_length=100,blank=False,null=False)
    email = models.EmailField(unique=True,blank=False,null=False)
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.name
    
class Employee(BaseClass):
    pass

class EmployeePersonalInfo(BaseClass):
    pass
    