from django.db import models

# Create your models here.
class Courses(models.Model):
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name
    
class Semesters(models.Model):
    SEMESTER_CHOICES = (
        ('1st', 'I'),
        ('2nd', 'II'),
        ('3rd', 'III'),
        ('4th', 'IV'),
        ('5th', 'V'),
        ('6th', 'VI'),
        ('7th', 'VII'),
        ('8th', 'VIII'),
    )

    semester = models.CharField(max_length=5, choices=SEMESTER_CHOICES, unique=True)

    def __str__(self):
        return self.semester