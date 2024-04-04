from django import forms
from .models import *

# FILE FORM 

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'

class LessonTimeForm(forms.ModelForm):
    class Meta:
        model = LessonTime
        fields = ['period', 'start_time', 'end_time']

        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id', 'name', 'classroom']

class ClassoomSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassroomSubject
        fields = '__all__'
        filter_horizontal = ['subject']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields ='__all__'
    
class SchoolYearForm(forms.ModelForm):
    class Meta:
        model = SchoolYear
        fields =['name']
    

class SemesterSelectionForm(forms.Form):
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label="Chọn Kì Học")