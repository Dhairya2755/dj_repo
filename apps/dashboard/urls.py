from django.contrib import admin
from django.urls import path 
from .views import *
urlpatterns = [
    path('',register,name="register"),
    path('inner/',index_inner,name='index_inner'),
    path('login/', login, name='login'),
]
    # path('outer/',index_outer,name='index_outer.html'),

