from django.contrib import admin
from django.urls import path 
from .views import *
urlpatterns = [
    path('', register, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', index_inner, name='dashboard'),
    path('logout/', logout,name='logout'),
]
   

    # path('outer/',index_outer,name='index_outer.html'),


