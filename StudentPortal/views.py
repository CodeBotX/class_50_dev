from django.shortcuts import render,get_object_or_404
from .models import Parent
from SM.models  import Student
from SM.models  import Mark
from .serializers import MarkSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class StudentMarks(APIView):
    def get(self, request, student):
        student = get_object_or_404(Student, pk=student)
        marks = Mark.objects.filter(student=student)
        serializer = MarkSerializer(marks, many=True)
        return render(request, 'lookup.html', {'marks': serializer.data})