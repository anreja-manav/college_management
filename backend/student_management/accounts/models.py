from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from acedmics.models import Courses, Semesters


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Roles(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.role


class Account(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    objects = CustomUserManager() 

    def __str__(self):
        return self.email

class TeacherProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='teacher_profile')
    profile_pic = models.ImageField(upload_to='teacher_profiles/', blank=True, null=True)
    subject_specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)

    course_assigned = models.ForeignKey(
        Courses, 
        on_delete=models.CASCADE, 
        null= True, 
        blank = True, 
        related_name='assigned_teachers'
    )
    semester_assigned = models.ForeignKey(
        Semesters,
        on_delete=models.CASCADE,
        null= True,
        blank = True,
        related_name='assigned_teachers'
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"

    def save(self, *args, **kwargs):
        if self.user.role.role != 'teacher':
            raise ValueError("Only users with role 'teacher' can have a TeacherProfile.")
        super().save(*args, **kwargs)

class StudentProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='student_profile')
    picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    course_enrolled = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='student_profile')
    semester = models.ForeignKey(Semesters, on_delete=models.CASCADE, related_name='student_profile')
    roll_no = models.PositiveIntegerField()
    
    father_name = models.CharField(max_length=100, null=True, blank=True)
    father_occupation = models.CharField(max_length=50, null=True, blank=True)
    father_phone = models.CharField(max_length=10, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    mother_occupation = models.CharField(max_length=50, null=True, blank=True)
    mother_phone = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        unique_together = ('course_enrolled', 'semester', 'roll_no')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"

    def save(self, *args, **kwargs):
        if self.user.role.role != 'student':
            raise ValueError("Only users with role 'student' can have a StudentProfile.")
        super().save(*args, **kwargs)