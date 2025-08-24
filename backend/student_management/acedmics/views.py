from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Result, Courses
from .serializers import ResultSerializer, CourseSerializer

from accounts.utils import is_admin
from accounts.models import Account

# Create your views here.

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    #add result
    @action(detail=False, methods=['post'], url_path='add/result')
    def add_result(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        serializer = ResultSerializer(data = data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({"status": status.HTTP_201_CREATED, "user details":serializer.data})
        return Response(serializer.errors)

    #update result
    @action(detail=False, methods=['patch'], url_path='update/result')
    def update_result(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        student_id = request.data.get('student')

        if not student_id:
            return Response({'detail': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Result.objects.get(student_id=student_id)
        except Result.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResultSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # delete result
    @action(detail=False, methods=['delete'], url_path='delete/result')
    def delete_result(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        student_id = request.data.get('student')

        if not student_id:
            return Response({'detail': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Result.objects.get(student_id=student_id)
        except Result.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response({'detail': 'Result deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer

    #add course
    @action(detail=False, methods=['post'], url_path='add/course')
    def add_course(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        serializer = CourseSerializer(data = data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({"status": status.HTTP_201_CREATED, "user details":serializer.data})
        return Response(serializer.errors)

    # update course
    @action(detail=False, methods=['patch'], url_path='update/course')
    def update_course(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        course_id = request.data.get('id')

        if not course_id:
            return Response({'detail': 'Course Id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete course
    @action(detail=False, methods=['delete'], url_path='delete/course')
    def delete_course(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        course_id = request.data.get('id')

        if not course_id:
            return Response({'detail': 'Course Id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response({'detail': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    #list course
    @action(detail=False, methods=['get'], url_path='list/course')
    def list_course(self, request):
        
        courses = Courses.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)