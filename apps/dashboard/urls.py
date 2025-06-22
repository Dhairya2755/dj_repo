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
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('policy-and-circular/', policy_and_circular, name='policy_and_circular'),
    path('generalinfo/',generalinfo,name='generalinfo'),
    path('updategeneral/',updategeneral,name='updategeneral'),
    path('induction/',induction,name='induction'),
    path('qualification/', qualification_form, name='qualification'),

    ]
   

    # path('outer/',index_outer,name='index_outer.html'),


