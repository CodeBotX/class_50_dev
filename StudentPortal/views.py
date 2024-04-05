from django.shortcuts import render,get_object_or_404

from SM.models  import Student


# Create your views here.
def student_lookup(request, student):
    student = get_object_or_404(Student, id=student)
    marks = student.marks.all() 
    context = {
        'student': student, 'marks': marks
    }
    return render(request, 'lookup.html',context)