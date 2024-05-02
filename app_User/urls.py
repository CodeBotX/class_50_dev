
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('signup/', views.teacher_register, name='SignUp'),
    path('', views.teacher_login_home, name='Login'),  
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset_form.html'), name='password_reset'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password/password_reset_form.html',
             email_template_name='password/password_reset_email.html',
             subject_template_name='password/password_reset_subject.txt',
             success_url='/password_reset/done/'
         ), 
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
]
