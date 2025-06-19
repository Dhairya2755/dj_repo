# admin.py — Correct way
from django.contrib import admin
from .models import UserRegistration

@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password')  # customize as needed
