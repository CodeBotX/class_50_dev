from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']  # Giả sử rằng Subject có trường 'name'

admin.site.register(LessonTime)

admin.site.register(SchoolYear)
admin.site.register(Semester)
admin.site.register(Mark)
admin.site.register(Student)
admin.site.register(Schedule)
@admin.register(ClassroomSubject)
class ClassroomSubjectAdmin(admin.ModelAdmin):
    list_display = ['classroom']
    filter_horizontal = ['subject']

# admin.site.register(CurrentSemester)
