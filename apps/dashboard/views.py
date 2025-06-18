from .models import UserRegistration
import re
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index_inner(request):
    return render(request,'dashboard/index_inner.html')

# def index_outer(request):
#     return render(request,'index_outer.html')

def register(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        return HttpResponse(f"Registered: {fullname} with email {email}")
    
    return render(request, 'dashboard/register.html')



def validate_password(password):
  
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"\d", password):
        return "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

def register(request):
    if request.method == "POST":
        fullname_ = request.POST.get("fullname")
        email_ = request.POST.get("email")
        password_ = request.POST.get("password")
        confirm_password_ = request.POST.get("confirm_password")


        if password_ != confirm_password_:
            return render(request, 'dashboard/register.html')
        
        UserRegistration.objects.create(
            fullname=fullname_,
            email=email_,
            password=password_  
        )
        UserRegistration.save()
        return render(request, 'dashboard/register.html')

    return render(request, 'dashboard/login.html')

# myapp/views.py

from django.shortcuts import render, redirect

def login(request):
    if request.method == 'POST':
        email_ = request.POST.get('email')
        password_ = request.POST.get('password')

    return render(request, 'dashboard/login.html')

def index_inner_view(request):
    return render(request, 'dashboard/index_inner.html')

