from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.teacher_register, name='SignUp'),
    path('', views.teacher_login_home, name='Login'),  
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name="logout"),
]
