from django.urls import path
from .views import AttendanceViewSet

get_students = AttendanceViewSet.as_view({'get': 'get_students'})
mark_attendance = AttendanceViewSet.as_view({'post': 'mark_attendance'})

urlpatterns = [
    path('attendance/mark/', mark_attendance, name='mark-attandance'),
    path('attendance/students/list/', get_students, name='student-list'),
]