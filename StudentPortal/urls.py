from django.urls import path
from . import views

urlpatterns = [  
    path('<int:student>/', views.student_lookup, name= 'Lookup'), 

]
