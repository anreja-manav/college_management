from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Attendance
from .serializers import AttendanceSerializer, BulkAttendanceSerializer
from accounts.models import StudentProfile
from accounts.utils import is_admin, is_teacher, is_student

# Create your views here.

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Attendance.objects.all()

        elif is_teacher(user):
            tp = user.teacher_profile
            return Attendance.objects.filter(course=tp.course_assigned, semester=tp.semester_assigned)

        elif is_student(user):
            return Attendance.objects.filter(student=user.student_profile)

        return Attendance.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if not is_teacher(user):
            raise PermissionError("Only teachers can create attendance.")

        tp = user.teacher_profile
        serializer.save(
            teacher=tp,
            course=tp.course_assigned,
            semester=tp.semester_assigned
        )

    @action(detail=False, methods=['post'], url_path='attendance/mark')
    def mark_attendance(self, request):
        if not is_teacher(request.user):
            return Response({"detail": "Only teachers can mark attendance."}, status=403)

        serializer = BulkAttendanceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            records = serializer.save()
            output_serializer = AttendanceSerializer(records, many=True)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='attendance/students/list')
    def get_students(self, request):
        if not is_teacher(request.user):
            return Response({"detail": "Only teachers can view this list."}, status=403)

        tp = request.user.teacher_profile
        students = StudentProfile.objects.filter(course_enrolled=tp.course_assigned, semester=tp.semester_assigned)

        data = [
            {"student_id": s.id, "name": f"{s.user.first_name} {s.user.last_name}", "email": s.user.email, "roll_no": s.roll_no}
            for s in students
        ]
        return Response(data, status=200)