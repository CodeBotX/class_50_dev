# 
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib import messages




# 
def teacher_register(request):
  form = SignUpForm()
  template = loader.get_template('signup.html')
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      # Thông báo thành công sau khi đăng kí
      messages.success(request, 'Thành công!')
      return HttpResponseRedirect(request.path_info)
  
  teachers = Teacher.objects.all()
  context = {
    'signupForm': form,
    'teachers':teachers
  }
  return HttpResponse(template.render(context,request))



def teacher_login_home(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        lookup_form = StudentLookupForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('home/')  # Thay đổi thành URL của trang thành công
        elif lookup_form.is_valid():
            action = request.POST.get('action')  # Lấy giá trị của action từ form
            if action == 'check':  # Đổi thành 'check'
                student_id = lookup_form.cleaned_data['student_id']
                return redirect('Lookup', student=student_id)
    else:
        login_form = LoginForm()
        lookup_form = StudentLookupForm()
    return render(request, 'login.html', {'loginForm': login_form, 'lookupForm': lookup_form})
  
  
  
      