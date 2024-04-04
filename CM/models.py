from django.db import models
from django.core.exceptions import ValidationError
from SM.models import Subject
from SM.models import Student
from SM.models import Classroom
from django.db.models.signals import post_save
from django.dispatch import receiver

  

# Tiết học
class Lessons (models.Model):
    name = models.CharField(max_length=150)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE) 
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    teacher = models.ForeignKey('app_User.Teacher', on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=1)  # Thêm trường counter (đếm số tiết) editable=False
    comment = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    grades = (
        (10, 'Tốt'),
        (8, 'Khá'),
        (6, 'Trung Bình'),
        (4, 'Yếu'),
    )
    grade = models.IntegerField(choices=grades, default='10')

    def __str__(self):
        return f"Tiết học: {self.name} Lớp: {self.classroom}" 
    
    def clean(self):
        if not self.grade:
            raise ValidationError("Bạn chưa chấm điểm bài học!")
    def save(self, *args, **kwargs):
        if not self.pk:  # Nếu đây là một tiết học mới
            last_lesson = Lessons.objects.filter(classroom=self.classroom, subject=self.subject).order_by('-counter').first()
            if last_lesson:
                self.counter = last_lesson.counter + 1
            else:
                self.counter = 1  # Đặt counter = 1 nếu đây là tiết học đầu tiên
        super().save(*args, **kwargs)

#Lưu chỗ ngồi        
class Seat(models.Model): 
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='seats')
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True,related_name='seat')
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    def __str__(self):
        return f"Cột {self.row}, Hàng {self.column}"
    def is_empty(self):
        return self.student is None
    class Meta:
        # Đảm bảo rằng mỗi vị trí trong lớp học là duy nhất.
        unique_together = [['classroom', 'row', 'column']]
    def assign_student(self, student):
        current_seat_of_student = Seat.objects.filter(student=student).first()
        if current_seat_of_student:
            # Đặt student hiện tại của seat này thành None để "trống" chỗ ngồi
            current_seat_of_student.student = None
            current_seat_of_student.save()

        # Gán chỗ ngồi mới cho học sinh
        self.student = student
        self.save()



@receiver(post_save, sender=Classroom)
def create_seats(sender, instance, created, **kwargs):
    if created:
        rows = 5
        columns = 8
        for row in range(1, rows + 1):
            for column in range(1, columns + 1):
                seat_number = (row - 1) * columns + column
                Seat.objects.create(classroom=instance, row=row, column=column)

