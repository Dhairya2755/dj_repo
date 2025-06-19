from django.contrib import admin
from django.urls import path 
from .views import *
urlpatterns = [
  #path('', register, name='register'),
   # path('login/', login_view, name='login'),
   path('', verification, name='verification'),
    path('emplogin/', employeelogin, name='emplogin'),
    path('index_inner/', index_inner, name='index_inner'),
    path('logout/', logout, name='logout'),
    ]
   

    # path('outer/',index_outer,name='index_outer.html'),


