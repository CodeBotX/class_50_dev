from django.db import models

# Create your models here.

class Parent(models.Model):
    id = models.CharField(max_length = 10, primary_key=True)
    name = models.CharField(max_length=100,blank = False, null =False)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    student_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def change_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number
        self.save()

    def change_pass(self, new_pass):
        self.password = new_pass
        self.save()