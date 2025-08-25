from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.utils import timezone
from datetime import datetime

from .models import Attendance
from .serializers import AttendanceSerializer
from accounts.models import StudentProfile
from accounts.utils import is_teacher
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['post'], url_path='attendance/mark')
    def mark_attendance(self, request):
        if not is_teacher(request.user):
            return Response({"detail": "Only teachers can mark attendance."}, status=403)

        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Expected a list of attendance records."}, status=400)

        teacher_profile = request.user.teacher_profile
        saved_records = []

        try:
            with transaction.atomic():
                for record in data:
                    student_id = record.get("student")
                    date = record.get("date") or timezone.now().date()

                    attendance, created = Attendance.objects.get_or_create(
                        student_id=student_id,
                        date=date,
                        defaults={
                            "teacher": teacher_profile,
                            "course": teacher_profile.course_assigned,
                            "semester": teacher_profile.semester_assigned,
                            "status": record.get("status", "present")
                        }
                    )

                    if not created:
                        attendance.status = record.get("status", attendance.status)
                        attendance.save()

                    saved_records.append(attendance)

        except Exception as e:
            return Response({"error": f"Failed to mark attendance: {str(e)}"}, status=400)

        return Response(AttendanceSerializer(saved_records, many=True).data, status=201)


    @action(detail=False, methods=['get'], url_path='view/attendance')
    def view_attendance(self, request):
        if not is_teacher(request.user):
            return Response({"detail": "Only teachers can view attendance."}, status=403)

        tp = request.user.teacher_profile
        if not tp.course_assigned or not tp.semester_assigned:
            return Response({"detail": "Teacher has no course/semester assigned."}, status=400)

        filters = {
            "student__course_enrolled": tp.course_assigned,
            "student__semester": tp.semester_assigned
        }
        date_str = request.query_params.get("date")
        if date_str:
            try:
                filters["date"] = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        attendances = Attendance.objects.filter(**filters).select_related("student__user")
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='attendance/students/list')
    def get_students(self, request):
        if not is_teacher(request.user):
            return Response({"detail": "Only teachers can view the list."}, status=403)

        tp = request.user.teacher_profile

        if not tp.course_assigned or not tp.semester_assigned:
            return Response({"detail": "Teacher has no course/semester assigned."}, status=400)

        students = StudentProfile.objects.filter(
            course_enrolled=tp.course_assigned,
            semester=tp.semester_assigned
        )

        data = [
            {
                "student_id": s.id,
                "name": f"{s.user.first_name} {s.user.last_name}",
                "email": s.user.email,
                "roll_no": s.roll_no
            }
            for s in students
        ]
        return Response(data, status=200)