
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='Home'),
    path('<str:classroom_name>/schedule_api', ClassroomScheduleAPIView.as_view(), name='classroom_schedule_api'),
    path('<str:classroom>/', views.classroom, name= 'classroom'),
    path('<str:classroom>/summary/', views.summary_view, name= 'summary'), 
    path('<str:classroom>/<int:student>/', views.detail, name= 'details'),

]

