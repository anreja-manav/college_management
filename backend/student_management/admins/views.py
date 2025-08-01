from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import AdminSerializer, LoginSerializer
from .models import AdminProfile

# Create your views here.
class AdminViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminSerializer

    @action(detail = False, methods = ['post'], url_path='create')
    def create_admin(self, request):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        serializer = AdminSerializer(data = data)
        if serializer.is_valid():
            
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = AdminProfile.objects.get(email=email)
            except AdminProfile.DoesNotExist:
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
    
    @action(detail = False, methods = ['get'], url_path = 'list')
    def list_admin(self, request):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        obj = AdminProfile.objects.all()
        serializer = AdminSerializer(obj, many = True)
        return Response(serializer.data)
    
    @action(detail = True, methods = ['put'], url_path = 'update')
    def update_admin(self, request, pk= None):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            instance = AdminProfile.objects.get(pk=pk)
        except AdminProfile.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminSerializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail = True, methods = ['patch'], url_path = 'partial_update')
    def partial_update_admin(self, request, pk= None):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            instance = AdminProfile.objects.get(pk=pk)
        except AdminProfile.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_admin(self, request, pk=None):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            instance = AdminProfile.objects.get(id=pk)
        except AdminProfile.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'detail': 'Admin deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
