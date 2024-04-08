
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('signup/', views.teacher_register, name='SignUp'),
    path('', views.teacher_login_home, name='Login'),  
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
