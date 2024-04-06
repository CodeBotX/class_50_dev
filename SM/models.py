from django.db import models
from .models import *
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


# Môn Học
class Subject (models.Model):
    id = models.CharField(primary_key=True, max_length = 10)
    name = models.CharField(max_length = 100,blank=False, null=False) # cần đảm bảo bắt buôc phải có
    def __str__(self):
        return f"{self.id}-{self.name}"

# Lớp Học
class Classroom(models.Model):
    name = models.CharField(primary_key=True,max_length=10)
    manager = models.ForeignKey('app_User.Teacher', on_delete=models.CASCADE,related_name='classroom') # 1 lớp chỉ có 1 giáo viên và ngược lại 
    def __str__(self):
        return self.name

# Môn Học Thuộc Lớp Học
class ClassroomSubject(models.Model):
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE,related_name='subjects')
    subject = models.ManyToManyField(Subject,blank=True,related_name='classroom_subjects')
    def __str__(self):
        return f"{self.classroom} - {self.subject}"

#  Học Sinh
class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100,blank=False, null=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='student') # cho phép classroom truy vấn được các student của mình
    def __str__(self):
        return f"{self.name} - ID: {self.id}" 


# Tiết Học
class LessonTime(models.Model):
    period = models.CharField(max_length=10, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    # def clean(self):
    # # Chuyển đổi start_time và end_time thành đối tượng datetime.time
    #     start_time = datetime.strptime(str(self.start_time)).time()
    #     end_time = datetime.strptime(str(self.end_time)).time()

    #     # Kiểm tra xem start_time có trước end_time không
    #     if start_time >= end_time:
    #         raise ValidationError(('Thời Gian Bắt Đầu Phải Trước Thời Gian Kết Thúc'))

    def __str__(self):
        return f"{self.period}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"



class Schedule(models.Model):
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetable')
    dayofweek = models.IntegerField(choices=DAY_CHOICES)
    period = models.ForeignKey(LessonTime, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,default="Trống")
    class Meta:
        # Đảm bảo rằng chỉ có một bản ghi cho mỗi cặp classroom, dayofweek và period
        unique_together = ['classroom', 'dayofweek', 'period']
 

# Năm học
class SchoolYear(models.Model):
    name = models.CharField(max_length=9)
    def validate_school_year_format(self):
        # Kiểm tra định dạng của 'name' để đảm bảo nó phù hợp với "YYYY-YYYY"
        if len(self.name) != 9 or self.name[4] != '-':
            return False
        start_year, end_year = self.name.split('-')
        if not (start_year.isdigit() and end_year.isdigit()):
            return False
        if int(end_year) - int(start_year) != 1:
            return False
        return True
    def save(self, *args, **kwargs):
        # Kiểm tra định dạng của 'name' trước khi lưu
        if not self.validate_school_year_format():
            raise ValidationError("'YYYY-YYYY'")
        super().save(*args, **kwargs)

# kì học
class Semester(models.Model):
    name = models.CharField(max_length=30)
    school_year = models.ForeignKey(SchoolYear,on_delete=models.CASCADE, related_name='schoolyear')
@receiver(post_save, sender=SchoolYear)
def create_semesters(sender, instance, created, **kwargs):
    if created:
        # Tạo 3 kì học khi năm học được tạo
        for i in range(1, 4):
            semester_name = f"{instance.name}-{i}"
            Semester.objects.create(name=semester_name, school_year=instance)

# Bảng Điểm 
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='marks')
    subject= models.ForeignKey(Subject, on_delete=models.CASCADE)
    scores = models.FloatField(models.FloatField(), blank=True, null=True)

    


    
