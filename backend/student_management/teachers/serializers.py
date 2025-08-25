from rest_framework import serializers
from .models import Attendance
from accounts.models import StudentProfile

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    roll_no = serializers.CharField(source="student.roll_no", read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'student',
            'student_name',
            'roll_no',
            'date',
            'status',
            'teacher',
            'course',
            'semester',
        ]

