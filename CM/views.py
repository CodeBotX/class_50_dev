from django.shortcuts import render,redirect
from django.template import loader
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404, render
from SM.models import Classroom
from SM.models import LessonTime 
from SM.models import Student
from SM.models import *
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from django.utils.dateparse import parse_time
from django.utils import timezone
from django.http import HttpResponseRedirect
day_names = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]


@login_required(login_url='/')
# home - chọn lớp học, dạy học or tổng kết
def home(request):
    # Giáo viên chọn Lớp học
    template = loader.get_template('home.html')
    if request.method == 'GET':
        classroom = request.GET.get('classroom')
        action = request.GET.get('action')
        if classroom:
            if action == 'Dạy Học':
                return redirect('classroom', classroom=classroom)
            elif action == 'Tổng Kết':
                return redirect('summary', classroom=classroom)
    classrooms = Classroom.objects.all()
    return render(request, 'home.html', {'classrooms': classrooms})


# Thêm Điểm
def add_mark(request):
    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            mark = form.cleaned_data['mark']
            # Thực hiện logic để thêm điểm vào cơ sở dữ liệu ở đây
            # Đừng quên lấy thông tin về student và subject từ request
            return redirect('success_url')  # Redirect người dùng sau khi thành công
    else:
        form = MarkForm()

    return render(request, 'testForm.html', {'add_markForm': form})

# classroom  - Hiển thị sơ đồ lớp, Môn Học, Tiết Học, Kì học
def classroom(request, classroom):
    # Hiển thị học sinh trong lớp
    classroom = get_object_or_404(Classroom, name=classroom) # đưa vào add lesson
    seats = classroom.seats.all().order_by('row', 'column') # đưa vào add lesson
    now_schedule = get_nowschedule(classroom=classroom)
    now = datetime.now()
    # Lấy thứ
    day_number = datetime.now().weekday()
    day_name = day_names[day_number]
    teacher = teacher = request.user
    if request.method == 'POST':
        form_addlesson = LessonForm(request.POST, teacher=teacher)
    # Xử lý thêm bài học
        if form_addlesson.is_valid():
            if now_schedule:
                lesson = form_addlesson.save(commit=False)
                lesson.classroom = classroom
                lesson.subject = now_schedule.subject
                lesson.save()
                messages.success(request, 'Thành công!')
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, 'Hiện không trong giờ dạy')
                return HttpResponseRedirect(request.path_info)
    else:
        form_addlesson = LessonForm(teacher=teacher)
        
    context = {
        'rows': range(1, 6),
        'columns': range(1, 9),
        'classroom': classroom,
        'seats':seats,
        'now':now,
        'now_schedule':now_schedule,
        'day_of_week':day_name,
        'form_addlesson': form_addlesson,
    }
    return render(request, 'classroom.html', context)

# API Lấy Tiết Học Hiện Tại 
class ClassroomScheduleAPIView(APIView):
    def get(self, request, classroom_name):
        client_time = request.GET.get('time')
        if client_time:
            current_time = parse_time(client_time)
        else:
            now = datetime.now()  # Sử dụng datetime.now() để lấy thời gian hiện tại
            current_time = now.time()
        
        classroom = Classroom.objects.get(name=classroom_name)
        
        # Xác định ngày trong tuần hiện tại
        dayofweek = datetime.today().weekday()  # 0 là Thứ Hai, 6 là Chủ Nhật

        schedule = Schedule.objects.filter(
            classroom=classroom,
            dayofweek=dayofweek,
            period__start_time__lte=current_time,
            period__end_time__gte=current_time
        ).first()

        if schedule:
            data = {
                'current_period': schedule.period.period,
                'subject': schedule.subject.name,
            }
        else:
            data = {
                'message': 'No classes at the moment.'
            }
        return Response(data)
    

# Trả về tiết học ở thời gian thực 
def get_nowschedule(classroom):
    dayofweek = datetime.now().weekday()
    now = datetime.now()
    # Truy vấn database để tìm tiết học mà thời gian hiện tại nằm giữa thời gian bắt đầu và kết thúc
    period = LessonTime.objects.filter(start_time__lte=now, end_time__gte=now).first()
    schedule = Schedule.objects.filter(classroom=classroom,dayofweek=dayofweek, period=period).first()
    if schedule:
        return schedule
    else:
        return None
def get_nowsubject(classroom):
    dayofweek = datetime.now().weekday()
    now = datetime.now()
    # Truy vấn database để tìm tiết học mà thời gian hiện tại nằm giữa thời gian bắt đầu và kết thúc
    period = LessonTime.objects.filter(start_time__lte=now, end_time__gte=now).first()
    schedule = Schedule.objects.filter(classroom=classroom,dayofweek=dayofweek, period=period).first()
    if schedule:
        return schedule.subject
    else:
        return None


# Giáo viên xem bảng tổng kết tuần
def summary_view (request,classroom):
    classroom = get_object_or_404(Classroom, name=classroom) # đưa vào add lesson
    seats = classroom.seats.all().order_by('row', 'column') # đưa vào add lesson
    schedule = Schedule.objects.filter(classroom=classroom).first()
    students = classroom.student.all()
    subjects = classroom.subjects.all()
    lesson = get_lessons_week(classroom=classroom)
    avglessons = get_avglessons(classroom=classroom)
    # Đổi chỗ
    if request.method == 'POST':
        form = AssignStudentForm(classroom, request.POST)  
        if form.is_valid():
            seat = form.cleaned_data['seat']
            student = form.cleaned_data['student']
            seat.assign_student(student)
            # messages.success(request, 'Thành công!')
            return HttpResponseRedirect(request.path_info)

    else:
        form = AssignStudentForm(classroom=classroom)
    context = {
        'lessons':lesson,
        'classroom':classroom,
        'students':students,
        'subjects':subjects,
        'assign_studentForm': form,
        'seats':seats,
        'schedule':schedule,
        'rows': range(1, 6),
        'columns': range(1, 9),
        'avglessons':avglessons
    }
    return render(request, 'summary.html', context)

# Lấy những tết học trong tuần để hiển thị tại summary
def get_lessons_week(classroom):
    # Xác định ngày đầu tiên của tuần
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    # Xác định ngày cuối cùng của tuần
    end_of_week = start_of_week + timedelta(days=6)
    # Truy vấn các tiết học thuộc classroom và trong khoảng thời gian từ start_of_week đến end_of_week
    lessons_week = Lessons.objects.filter(classroom=classroom, date_time__date__range=[start_of_week, end_of_week])
    return lessons_week


# Thêm điểm cho học sinh trong khi đang học ( đang lỗi )
def detail(request,classroom,student):
    student = get_object_or_404(Student, pk=student)
    now_schedule = get_nowschedule(classroom=classroom)
    subject = now_schedule.subject
    if subject is None:
        messages.error(request, 'Bạn không đang trong giờ dạy!')
        return redirect('classroom', classroom=classroom)

    if request.method == 'POST':
        if subject:  # Kiểm tra lại để đảm bảo subject có tồn tại
            form = MarkForm(request.POST, student=student, subject=subject)
            if form.is_valid():
                form.save()
            else:
                messages.error(request, "Có lỗi xảy ra, vui lòng kiểm tra lại.")
        else:
            return redirect('classroom', classroom=classroom)
    else:
        form = MarkForm(student=student, subject=subject) if subject else None
    marks = student.marks.filter(student=student,subject=subject)
    context={
        'MarkForm': form,
        'student':student,
        'subject':subject,
        'marks': marks
    }
    return render(request, 'details.html', context)


def get_avglessons(classroom):  
    now = timezone.now()  
    # Lấy ngày đầu tuần (thứ Hai)
    start_of_week = now - timedelta(days=now.weekday())
    # Lấy ngày cuối tuần (Chủ Nhật)
    end_of_week = start_of_week + timedelta(days=6)
    # Lọc các tiết học trong tuần này thuộc lớp học đã chọn
    lessons_this_week = Lessons.objects.filter(date_time__range=[start_of_week, end_of_week], classroom=classroom)
    # Tính điểm trung bình của các tiết học trong lớp
    lesson_grades = lessons_this_week.aggregate(average_grade=Avg('grade'))
    return lesson_grades['average_grade']