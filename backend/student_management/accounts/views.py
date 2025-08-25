from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Account, Roles
from .serializers import AccountSerializer, LoginSerializer
from .utils import is_admin
from teachers.models import Attendance
from teachers.serializers import AttendanceSerializer

# Create your views here.
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    #login
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response({
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'User not found'
                })

            if not check_password(password, user.password):
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid Password'
                })

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    #Create Admin
    @action(detail = False, methods = ['post'], url_path='create/admin')
    def create_admin(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        serializer = AccountSerializer(data = data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({"status": status.HTTP_201_CREATED, "user details":serializer.data})
        return Response(serializer.errors)
    
    # List Admin
    @action(detail = False, methods = ['get'], url_path = 'list/admin')
    
    def list_admin(self, request):
        
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        admins = Account.objects.filter(role__role='admin')
        serializer = AccountSerializer(admins, many = True)
        return Response(serializer.data)
    
    #Update Admin
    @action(detail = False, methods = ['put'], url_path = 'update/admin')
    def update_admin(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Account.objects.get(email=email, role__role='admin')
        except Account.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partial Update Admin
    @action(detail = False, methods = ['patch'], url_path = 'partial_update/admin')
    def partial_update_admin(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Account.objects.get(email=email, role__role='admin')
        except Account.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Delete Admin
    @action(detail=False, methods=['delete'], url_path='delete/admin')
    def delete_admin(self, request):
        
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Account.objects.get(email=email, role__role='admin')
        except Account.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'detail': 'Admin deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



    #Create Teacher
    @action(detail=False, methods=['post'], url_path='create/teacher')
    def create_teacher(self, request):

        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            teacher_role = Roles.objects.get(role='teacher')
        except Roles.DoesNotExist:
            return Response({'detail': 'Teacher role not found in database.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['role'] = teacher_role.role

        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Teacher created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    #Teacher's List
    @action(detail = False, methods = ['get'], url_path = 'list/teacher')
    
    def list_teacher(self, request):
        
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        teachers = Account.objects.filter(role__role='teacher')
        serializer = AccountSerializer(teachers, many = True)
        return Response(serializer.data)
    
    #Update Teacher
    @action(detail = False, methods = ['put'], url_path = 'update/teacher')
    def update_teacher(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Account.objects.get(email=email, role__role='teacher')
        except Account.DoesNotExist:
            return Response({'detail': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partial Update Teacher
    @action(detail = False, methods = ['put'], url_path = 'partial_update/teacher')
    def partial_update_teacher(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Account.objects.get(email=email, role__role='teacher')
        except Account.DoesNotExist:
            return Response({'detail': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Delete Teacher
    @action(detail=False, methods=['delete'], url_path='delete/Teacher')
    def delete_teacher(self, request):
        
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Account.objects.get(email=email, role__role='teacher')
        except Account.DoesNotExist:
            return Response({'detail': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'detail': 'Teacher deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

    #Create Student
    @action(detail=False, methods=['post'], url_path='create/student')
    def create_student(self, request):

        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            student_role = Roles.objects.get(role='student')
        except Roles.DoesNotExist:
            return Response({'detail': 'Student role not found in database.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['role'] = student_role.role

        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Student created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    #Student's List
    @action(detail = False, methods = ['get'], url_path = 'list/student')
    
    def list_student(self, request):
        
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        students = Account.objects.filter(role__role='student')
        serializer = AccountSerializer(students, many = True)
        return Response(serializer.data)
    
    #Update Student
    @action(detail = False, methods = ['put'], url_path = 'update/student')
    def update_student(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Account.objects.get(email=email, role__role='student')
        except Account.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partial Update Student
    @action(detail = False, methods = ['put'], url_path = 'partial_update/student')
    
    def partial_update_student(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Account.objects.get(email=email, role__role='student')
        except Account.DoesNotExist:
            return Response({'detail': 'student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Delete Student
    @action(detail=False, methods=['delete'], url_path='delete/student')
    def delete_student(self, request):
        
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Account.objects.get(email=email, role__role='student')
        except Account.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'detail': 'Student deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    #view attendance
    @action(detail=False, methods=['get'], url_path='attendance/view')
    def view_attendance(self, request):
        if not is_admin(request.user):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        date = request.query_params.get("date")
        course = request.query_params.get("course")
        semester = request.query_params.get("semester")

        qs = Attendance.objects.all()

        if date:
            try:
                qs = qs.filter(date=parse_date(date))
            except Exception:
                return Response({"error": "Invalid date format, expected YYYY-MM-DD"}, status=400)

        if course:
            qs = qs.filter(course_id=course)

        if semester:
            qs = qs.filter(semester_id=semester)

        serializer = AttendanceSerializer(qs, many=True)
        return Response(serializer.data, status=200)