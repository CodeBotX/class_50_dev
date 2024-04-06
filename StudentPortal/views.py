from django.shortcuts import render,get_object_or_404
from SM.models import ClassroomSubject

from SM.models  import Student


# Create your views here.
def student_lookup(request, student):
    student = get_object_or_404(Student, id=student)
    marks = student.marks.all() 
    classroom = student.classroom
    classroomsubjects = ClassroomSubject.objects.filter(classroom=classroom).first()
    subjects = classroomsubjects.subject.all()
    marks_by_subject = {}
    for mark in marks:
        if mark.subject.name not in marks_by_subject:
            marks_by_subject[mark.subject.name] = [mark.scores]
        else:
            marks_by_subject[mark.subject.name].append(mark.scores)
    context = {
        'student': student, 
        'marks': marks,
        'student_of_subjects': subjects,
        'marks_by_subject': marks_by_subject,
    }
    return render(request, 'lookup.html',context)