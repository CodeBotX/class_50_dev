from django.contrib import admin
from .models import *



admin.site.register(Lessons)


class SeatAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'row', 'column', 'student')
    list_filter = ('classroom', 'column', 'row')  
admin.site.register(Seat, SeatAdmin)