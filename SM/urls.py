
from django.urls import path
from . import views

urlpatterns = [  
    path('', views.school_view, name='School'),
    path('subjects/', views.add_subject, name='smsubject'),
    path('classrooms/', views.add_and_set_classroom, name='smclassroom'),
    path('students/', views.add_student, name='smstudent'),
    path('timetable/', views.time_table, name='smtimetable'),
    path('timetable/', views.classroom_timetable, name='API_get_timetable'),
    path('rankings/', views.rank_classrooms_by_weekly_grades, name= 'rankclassrooms'),
]
