from django.db import models
from admins.models import Roles
from acedmics.models import Courses

# Create your models here.
class Students(models.Model):
    YEAR_CHOICES = (
        ('1st', 'I'),
        ('2nd', 'II'),
        ('3rd', 'III'),
        ('4th', 'IV')
    )
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    roll_no = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    alternate_phone = models.CharField(max_length=10, null=True, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    year = models.CharField(max_length=10, choices=YEAR_CHOICES, unique=True)
    address = models.TextField(max_length=200)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.course} - {self.year}"