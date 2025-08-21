from rest_framework.response import Response
from rest_framework import status

def is_admin(user):
    return user.is_authenticated and getattr(user.role, 'role', None) == 'admin'

def is_teacher(user):
    return user.is_authenticated and getattr(user.role, 'role', None) == 'teacher'

def is_student(user):
    return user.is_authenticated and getattr(user.role, 'role', None) == 'student'