from typing import Any
from django.db import models
from django.utils import timezone
# Create your models here.
# Người dùng là giáo viên

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

class TeacherManager(UserManager):
    def _create_user(self, email, id, password, **extra_fields):
        """
        Tạo và lưu một Teacher với email, teacher_id và mật khẩu cho trường hợp một user thông thường
        """
        if not email:
            raise ValueError('Email phải được cung cấp')
        email = self.normalize_email(email)
        user = self.model(email=email, id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False) # không phải là nhân viên 
        extra_fields.setdefault('is_superuser', False) # không phải là addmin
        return self._create_user(email, id, password, **extra_fields )

    def create_superuser(self, email, id, password=None, **extra_fields):
        """
        Tạo và lưu một Superuser với email, id và mật khẩu
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser phải là is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser phải là is_superuser=True.')

        return self._create_user(email, id, password, **extra_fields)

#Lưu giáo viên
class Teacher(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(blank = True, default="",unique=True)
    id = models.CharField(max_length=10, unique=True,primary_key=True)
    last_name = models.CharField(max_length = 100,blank =True, default="")
    first_name = models.CharField(max_length = 100,blank =True, default="")
    # profile_image = models.ImageField(max_length=255, upload_to=, null=True,blank=True)
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(default = timezone.now)
    
    objects = TeacherManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['id'] #id
    
    class Meta:
        verbose_name = 'Teacher_User'
        verbose_name_plural = 'Teacher_Users'
    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"
    def __str__(self):
        return self.id