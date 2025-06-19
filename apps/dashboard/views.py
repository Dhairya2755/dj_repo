from django.shortcuts import render,redirect
from .models import UserRegistration
import re

# Create your views here.

# def index_inner(request):
#     return render(request,'dashboard/index_inner.html')

# def index_outer(request):
#     return render(request,'index_outer.html')
def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"\d", password):
        return "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

# Register View
def register(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        error = validate_password(password)
        if error:
            return render(request, 'dashboard/register.html', {"error": error})

        if password != confirm_password:
            return render(request, 'dashboard/register.html', {"error": "Passwords do not match."})

        UserRegistration.objects.create(
            fullname=fullname,
            email=email,
            password=password
        )
        return redirect('login')  # Go to login after registration

    return render(request, 'dashboard/register.html')

# Login View
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Simple database check
        user = UserRegistration.objects.filter(email=email, password=password).first()
        if user:
            return redirect('index_inner')
        else:
            return render(request, 'dashboard/login.html', {'error': 'Invalid credentials'})

    return render(request, 'dashboard/login.html')

# Dashboard
def index_inner(request):
    return render(request, 'dashboard/index_inner.html')

#logout
def logout(request):
    # del request.session['']
    #return redirect(request,'dashboard/register.html')
    #return redirect(request,'dashboard/login.html')
    return redirect ('login')