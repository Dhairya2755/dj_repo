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
