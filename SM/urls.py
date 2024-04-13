
from django.urls import path
from . import views

urlpatterns = [  
    path('', views.school_view, name='School'),
    path('subjects/', views.add_subject, name='smsubject'),
    path('classrooms/', views.add_and_set_classroom, name='smclassroom'),
    path('students/', views.manage_students, name='smstudent'),
    path('timetable/', views.timetable, name='smtimetable'),
    path('rankings/', views.rank_classrooms_by_weekly_grades, name= 'rankclassrooms'),
]
