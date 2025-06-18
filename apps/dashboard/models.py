from django.db import models

# Create your models here.

class UserRegistration(models.Model):
    fullname = models.CharField(max_length=100,blank=False,null=False)
    email = models.EmailField(unique=True,blank=False,null=False)
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.fullname
