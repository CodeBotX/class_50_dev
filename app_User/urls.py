from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.teacher_register, name='SignUp'),
    path('', views.teacher_login_home, name='Login'),  
]
