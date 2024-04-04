from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Avg
from datetime import datetime, timedelta
from CM.models import Lessons
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def school_view(request):
    if request.method == 'POST':
        form = SemesterSelectionForm(request.POST)
        if form.is_valid():
            # Lưu lựa chọn vào session
            request.session['current_semester_id'] = form.cleaned_data['semester'].id
            return redirect('School')
    else:
        form = SemesterSelectionForm()
    return render(request, 'school.html', {'form': form})


# Thêm môn học (0k)
def add_subject(request):
    subjects= Subject.objects.all()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Thêm môn học thành công!')
    else:
        form = SubjectForm()
    context = {
        'add_subjectsform': form,
        'subjects':subjects
    }
    return render(request, 'subjects.html', context)


# Thêm lớp học ( chưa xong )
def add_and_set_classroom(request):
    classrooms = Classroom.objects.all()
    if request.method == 'POST':
        form_Classroom = ClassroomForm(request.POST)
        form_Subject = ClassoomSubjectForm(request.POST)
        if form_Classroom.is_valid():
            action = request.POST.get('action')
            if action == 'addclassroom':
                form_Classroom.save()
                messages.success(request, 'Thêm lớp học thành công!')
        elif form_Subject.is_valid():
            action = request.POST.get('action')
            if action == 'setsubject':
                form_Subject.save()
                messages.success(request,'Thành Công')
    else:
        form_Classroom = ClassroomForm()
        form_Subject = ClassoomSubjectForm()
    context = {
        'classroom':classrooms,
        'classroomForm': form_Classroom,
        'subjectsForm':form_Subject
    }
    return render(request, 'classrooms.html',context)


# Thêm học sinh (OK)
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm học sinh thành công!')
            students = Student.objects.all()
            return render(request, 'student_list.html', {'students': students})
    else:
        form = StudentForm()
    
    classrooms = Classroom.objects.all()
    
    context ={
        'StudentForm': form,
        'classrooms':classrooms,
    }

    return render(request, 'students.html', context)

def get_students(request):
    classroom_id = request.GET.get('classroom_id')
    if classroom_id:
        students = Student.objects.filter(classroom__name=classroom_id)
    else:
        students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


# Thêm lịch học
def time_table (request):
    if request.method == 'POST':
        form_lessons = LessonTimeForm()
        form_schedules = ScheduleForm()
        if form_lessons.is_valid():
            action = request.POST.get('action')
            if action == 'lesson':
                form_lessons.save()
                messages.success(request, 'Thành Công')
        elif form_schedules.is_valid():
            if action == 'schedule':
                try:
                    form_schedules.save()
                    messages.success(request, 'Thêm lịch học thành công!')
                except IntegrityError:
                    messages.error(request, 'Đã tồn tại!')
    else:
        form_lessons = LessonTimeForm()
        form_schedules = ScheduleForm()
    return render(request, 'timetable.html', {'form_lessons': form_lessons,'form_schedules':form_schedules})

# Hiện thị thời khóa biểu ( đang sửa, chưa update)
def classroom_timetable(request):
    # Lấy tên lớp học từ query parameters
    classroom_name = request.GET.get('classroom', None)

    # Khởi tạo các biến cần thiết
    schedules = None
    selected_classroom = None

    # Lấy tất cả các lớp học để hiển thị trong dropdown
    classrooms = Classroom.objects.all()

    # Kiểm tra xem có tên lớp học được chọn không
    if classroom_name:
        # Lấy đối tượng Classroom dựa trên tên
        selected_classroom = get_object_or_404(Classroom, name=classroom_name)
        # Lấy các lịch học liên quan đến lớp học được chọn
        schedules = Schedule.objects.filter(classroom=selected_classroom).select_related('subject', 'period')

    return render(request, 'timetable.html', {
        'selected_classroom': selected_classroom,  # Đối tượng lớp học được chọn
        'schedules': schedules,  # Các lịch học liên quan
        'classrooms': classrooms  # Danh sách tất cả các lớp học
    })
        
        
def rank_classrooms_by_weekly_grades(request):
    # Lấy ngày đầu tuần (thứ Hai)
    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
    # Lấy ngày cuối tuần (Chủ Nhật)
    end_of_week = start_of_week + timedelta(days=6)

    # Lọc các tiết học trong tuần này
    lessons_this_week = Lessons.objects.filter(date_time__range=[start_of_week, end_of_week])

    # Tính điểm trung bình của mỗi lớp học
    classroom_grades = lessons_this_week.values('classroom').annotate(average_grade=Avg('grade'))

    # Sắp xếp các lớp học theo điểm trung bình từ cao đến thấp
    ranked_classrooms = sorted(classroom_grades, key=lambda x: x['average_grade'], reverse=True)
    return render(request, 'rank_classrooms.html', {'ranked_classrooms': ranked_classrooms})
    