
from django.urls import path
from . import views
from .views import export_lessons_pdf,preview_lessons

urlpatterns = [  
    path('', views.school_view, name='School'),
    path('export_lessons_pdf/', export_lessons_pdf, name='export_lessons_pdf'),
    path('lessons/preview/', preview_lessons, name='preview_lessons'),
    path('subjects/', views.add_subject, name='smsubject'),
    path('classrooms/', views.add_and_set_classroom, name='smclassroom'),
    path('students/', views.manage_students, name='smstudent'),
    path('timetable/', views.timetable, name='smtimetable'),
    path('rankings/', views.rank_classrooms_by_weekly_grades, name= 'rankclassrooms'),
]
