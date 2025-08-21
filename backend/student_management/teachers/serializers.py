from rest_framework import serializers
from .models import Attendance
from accounts.models import StudentProfile

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['teacher', 'course', 'semester']

class BulkAttendanceStudentSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Attendance.STATUS_CHOICES)
    remarks = serializers.CharField(required=False, allow_blank=True)

class BulkAttendanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    students = BulkAttendanceStudentSerializer(many=True)

    def create(self, validated_data):
        teacher = self.context['request'].user
        teacher_profile = teacher.teacher_profile
        course = teacher_profile.course_assigned
        semester = teacher_profile.semester_assigned

        attendance_records = []
        for student_data in validated_data['students']:
            try:
                student = StudentProfile.objects.get(id=student_data['student_id'])
            except StudentProfile.DoesNotExist:
                raise serializers.ValidationError(
                    {"student_id": f"Student with id {student_data['student_id']} not found"}
                )

            record, _ = Attendance.objects.update_or_create(
                student=student,
                date=validated_data['date'],
                defaults={
                    'teacher': teacher_profile,
                    'course': course,
                    'semester': semester,
                    'status': student_data['status'],
                    'remarks': student_data.get('remarks', "")
                }
            )
            attendance_records.append(record)

        return attendance_records

    # def to_representation(self, instance):
    #     """
    #     Handle both single Attendance and list of Attendance objects
    #     """
    #     if isinstance(instance, list):
    #         return AttendanceSerializer(instance, many=True).data
    #     return AttendanceSerializer(instance).data
