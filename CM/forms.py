
'''
Form add lesson
Form add điểm
Form lựa chọn lớp học

'''

from django import forms
from django.core.exceptions import ValidationError
from .models import *
from SM.models import Mark

#Nhập điểm
class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['scores']  # Chỉ cho phép người dùng nhập điểm

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)
        # self.instance.student = student
        # self.instance.subject = subject 
        if subject and student:
            self.instance.student = student
            self.instance.subject = subject
        else:
            # Xử lý trường hợp subject hoặc student không hợp lệ
            # Bạn có thể set self.instance là None hoặc thêm các lỗi vào form
            self.add_error(None, "Không tìm thấy thông tin hợp lệ để thêm điểm.")
        


# Form chọn lớp học
class ClassroomSelectionForm(forms.Form):
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all(), empty_label=None, label='Select_Classroom')
    
# Form add lession

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lessons
        fields = ['name', 'comment', 'grade']

    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher', None)
        super(LessonForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(LessonForm, self).save(commit=False)
        instance.teacher = self.teacher
        if commit:
            instance.save()
        return instance
    

# Đổi chỗ ngồi 
# class AssignStudentForm(forms.Form):
#     seat = forms.ModelChoiceField(queryset=seats) 
#     student = forms.ModelChoiceField(queryset=students)  


class AssignStudentForm(forms.Form):
    def __init__(self, classroom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # lấy seats và students thuộc cùng 1 lớp 
        seats = Seat.objects.filter(classroom=classroom)
        students = Student.objects.filter(classroom=classroom)
        # Cập nhật trường queryset cho seat và student
        self.fields['seat'] = forms.ModelChoiceField(queryset=seats)
        self.fields['student'] = forms.ModelChoiceField(queryset=students)

    seat = forms.ModelChoiceField(queryset=Seat.objects.none())  # Trường rỗng ban đầu
    student = forms.ModelChoiceField(queryset=Student.objects.none())  # Trường rỗng ban đầu