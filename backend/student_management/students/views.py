from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from accounts.utils import is_student
from acedmics.serializers import ResultSerializer
from acedmics.models import Result
from teachers.models import Attendance
from teachers.serializers import AttendanceSerializer

# Create your views here.
class StudentDashboardViewSet(viewsets.ModelViewSet):

    #Result
    @action(detail=False, methods=['get'], url_path='result')
    def show_result(self, request):
        if not is_student(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        results = Result.objects.filter(student=request.user.student_profile)
        if not results.exists():
            return Response(
                {'detail': 'No results found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
    
    #attendance
    @action(detail=False, methods=['get'], url_path='attendance')
    def show_attendance(self, request):
        if not is_student(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        attendances = Attendance.objects.filter(student = request.user.student_profile)
        if not attendances.exists():
            return Response(
                {'detail': 'No record found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)