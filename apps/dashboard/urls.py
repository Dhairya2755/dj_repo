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
    path('family_info/', family_info, name='family_info'),
   #path('generate_slip/', generate_salary_view, name='generate__view'),
    # path('salary_slips/', salary_slip_view, name='salary_slip_view'),
    path('loan-history/', loan_history_view, name='loan_history'),
    path('my-acceptance/', my_acceptance_view, name='my_acceptance'),
    path('proof_status/', proof_status_view, name='proof_status'),
    path('claims/', claims_view, name='claims_page'),
    path('claim-status/', claim_status_view, name='claim_status'), 
    path('salary/', salary_slip_list_view, name='salary'),
    path('generate-slip/', generate_salary_slip_pdf, name='generate_salary_slip'),
    path('apply-leave/', leave_apply_view, name='apply_leave'),
    path('leave-history/', leave_history_view, name='leave_history'),
 ]
   

    # path('outer/',index_outer,name='index_outer.html'),


