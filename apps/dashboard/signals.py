# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Employee, Salary

# @receiver(post_save, sender=Employee)
# def create_salary_on_employee_creation(sender, instance, created, **kwargs):
#     if created:
#         Salary.objects.create(employee=instance)
