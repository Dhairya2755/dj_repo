from django.contrib import admin
from django.urls import path 
from .views import *
urlpatterns = [
    path('',register,name="dashboard/register.html"),
    path('inner/',index_inner,name='dashboard/index_inner.html'),
]
    # path('outer/',index_outer,name='index_outer.html'),

