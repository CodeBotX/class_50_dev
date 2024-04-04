from django.urls import path
from . import views

urlpatterns = [  
    path('<int:student>/', views.StudentMarks.as_view(), name= 'Lookup'), 

]
