from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Avg
from datetime import datetime, timedelta
from CM.models import Lessons
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from CM.models import Lessons
from django.db import transaction

# Thay đổi thông tin học sinh
def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)  # Lấy đối tượng Student dựa trên ID
    old_classroom = student.classroom 
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            with transaction.atomic():
                student = form.save(commit=False)  # Lưu student tạm thời
                new_classroom = form.cleaned_data['classroom']  # Lấy thông tin lớp học mới từ form
                if old_classroom != new_classroom:
                    # Nếu lớp học thay đổi, gán trường student trong chỗ ngồi của học sinh là null
                    student.seat.update(student=None)
                student = form.save()  # Lưu thay đổi cuối cùng vào database
            return redirect('smstudent')  # Thay 'some_view_to_redirect' bằng tên view mà bạn muốn chuyển hướng sau khi cập nhật thành công
    else:
        form = StudentEditForm(instance=student)  # Khởi tạo form với thông tin học sinh sẵn có

    return render(request, 'edit/editStudent.html', {'form': form})


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


# Thêm lớp học 
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
                return HttpResponseRedirect(request.path_info)
        elif form_Subject.is_valid():
            action = request.POST.get('action')
            if action == 'setsubject':
                form_Subject.save()
                messages.success(request,'Thành Công')
                return HttpResponseRedirect(request.path_info)
    else:
        form_Classroom = ClassroomForm()
        form_Subject = ClassoomSubjectForm()
    context = {
        'classroom':classrooms,
        'classroomForm': form_Classroom,
        'subjectsForm':form_Subject
    }
    return render(request, 'classrooms.html',context)


# Thêm học sinh (OK) - chưa sử dụng
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm học sinh thành công!')
            students = Student.objects.all()
            return render(request, 'students.html', {'students': students})
    else:
        form = StudentForm()

    context ={
        'StudentForm': form
    }

    return render(request, 'students.html', context)

# add and show students
def manage_students(request):
    classrooms = Classroom.objects.all()
    classroom_id = request.GET.get('classroom_id')  # Mặc định là chuỗi rỗng nếu không tồn tại
    students = Student.objects.none()

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm học sinh thành công!')
            # Lấy URL hiện tại và redirect lại nó để ở lại trang
            current_url = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(current_url)
    else:
        form = StudentForm()
        if classroom_id:
            students = Student.objects.filter(classroom__name=classroom_id).select_related('classroom')

    context = {
        'students': students,
        'classrooms': classrooms,
        'StudentForm': form
    }

    if request.method == 'POST' and not form.is_valid():
        # Trường hợp request.method là 'POST' nhưng form không hợp lệ
        messages.error(request, 'Có lỗi xảy ra. ID đã được sử dụng.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'students.html', context)

# Thêm lịch học ( tạm thời chưa sử dụng)
def time_table (request):
    if request.method == 'POST':
        form_lessons = LessonTimeForm(request.POST)
        form_schedules = ScheduleForm(request.POST)
        if form_lessons.is_valid():
            action = request.POST.get('action')
            if action == 'lesson':
                form_lessons.save()
                messages.success(request, 'Thành Công')
                return HttpResponseRedirect(request.path_info)
        elif form_schedules.is_valid():
            if action == 'schedule':
                try:
                    form_schedules.save()
                    messages.success(request, 'Thêm lịch học thành công!')
                    return HttpResponseRedirect(request.path_info)
                except IntegrityError:
                    messages.error(request, 'Đã tồn tại!')
    else:
        form_lessons = LessonTimeForm()
        form_schedules = ScheduleForm()
    return render(request, 'timetable.html', {'form_lessons': form_lessons,'form_schedules':form_schedules})

# Hiện thị thời khóa biểu ( đang sửa, chưa update)
def show_timetable(request):
    classrooms = Classroom.objects.all()
    classroom_name = request.GET.get('classroom_name')
    schedule = None
    selected_classroom = None

    if classroom_name:
        selected_classroom = Classroom.objects.filter(classroom__name=classroom_name).first()
        if selected_classroom:
            schedule = Schedule.objects.filter(classroom=selected_classroom)
    return render(request, 'timetable.html', {
        'classrooms': classrooms,
        'selected_classroom': selected_classroom,
        'schedule': schedule,
    })

# Đang sử dụng
def timetable(request):
    classroom_name = request.GET.get('classroom_name')
    if request.method == 'POST':
        form_lessons = LessonTimeForm(request.POST)
        form_schedules = ScheduleForm(request.POST)
        if form_lessons.is_valid():
            action = request.POST.get('action')
            if action == 'lesson':
                form_lessons.save()
                messages.success(request, 'Thêm lịch học thành công!')
                return HttpResponseRedirect(f"{request.path_info}?classroom_name={classroom_name}")
        elif form_schedules.is_valid():
            action = request.POST.get('action')
            if action == 'schedule':
                form_schedules.save()
                messages.success(request,'Thành Công')
                return HttpResponseRedirect(f"{request.path_info}?classroom_name={classroom_name}")
    else:
        form_lessons = LessonTimeForm(request.POST)
        form_schedules = ScheduleForm(request.POST)
    classrooms = Classroom.objects.all()
    # classroom_name = request.GET.get('classroom_name')
    schedules = None
    schedules_2= None
    schedules_3 = None
    schedules_4 = None
    schedules_5 = None
    schedules_6 = None
    schedules_7 = None
    schedules_8 = None
    selected_classroom = None

    if classroom_name:
        selected_classroom = Classroom.objects.filter(name=classroom_name).first()
        if selected_classroom:
            # schedule = Schedule.objects.filter(classroom=selected_classroom)
            schedules = Schedule.objects.filter(classroom=selected_classroom).order_by('dayofweek', 'period__start_time')
            schedules_2 = Schedule.objects.filter(classroom=selected_classroom, dayofweek=0).order_by('period__start_time')
            schedules_3 = Schedule.objects.filter(classroom=selected_classroom, dayofweek=1).order_by('period__start_time')
            schedules_4 = Schedule.objects.filter(classroom=selected_classroom, dayofweek=2).order_by('period__start_time')
            schedules_5 = Schedule.objects.filter(classroom=selected_classroom, dayofweek=3).order_by('period__start_time')
            schedules_6 = Schedule.objects.filter(classroom=selected_classroom, dayofweek=4).order_by('period__start_time')
            schedules_7 = Schedule.objects.filter(classroom=selected_classroom, dayofweek=5).order_by('period__start_time')
            schedules_8 = Schedule.objects.filter(classroom=selected_classroom, dayofweek=6).order_by('period__start_time')
    return render(request, 'timetable.html', {
        'form_lessons': form_lessons,
        'form_schedules': form_schedules,
        'classrooms': classrooms,
        'selected_classroom': selected_classroom,
        'schedule': schedules,
        'schedule_2': schedules_2,
        'schedule_3': schedules_3,
        'schedule_4': schedules_4,
        'schedule_5': schedules_5,
        'schedule_6': schedules_6,
        'schedule_7': schedules_7,
        'schedule_8': schedules_8,
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

