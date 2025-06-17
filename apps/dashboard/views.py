from django.shortcuts import render

# Create your views here.
def index_inner(request):
    return render(request,'dashboard/index_inner.html')

# def index_outer(request):
#     return render(request,'index_outer.html')