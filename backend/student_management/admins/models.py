from django.db import models

# Create your models here.
class Roles(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.role

class AdminProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
