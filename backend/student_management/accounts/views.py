from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Account
from .serializers import AccountSerializer, LoginSerializer

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail = False, methods = ['post'], url_path='create')
    def create_admin(self, request):
        user = request.user
        if not user.is_authenticated or getattr(user.role, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        serializer = AccountSerializer(data = data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({"status": status.HTTP_201_CREATED, "user details":serializer.data})
        return Response(serializer.errors)
    
    
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
    
    @action(detail = False, methods = ['get'], url_path = 'list')
    
    def list_admin(self, request):
        
        user = request.user
        if not user.is_authenticated or getattr(user.role, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        obj = Account.objects.all()
        serializer = AccountSerializer(obj, many = True)
        return Response(serializer.data)
    
    @action(detail = True, methods = ['put'], url_path = 'update')
    def update_admin(self, request, pk= None):
        user = request.user
        if not user.is_authenticated or getattr(user.role, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            instance = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail = True, methods = ['patch'], url_path = 'partial_update')
    def partial_update_admin(self, request, pk):
        import pdb; pdb.set_trace()
        user = request.user
        if not user.is_authenticated or getattr(user.role, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            instance = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_admin(self, request, pk = None):
        
        user = request.user
        if not user.is_authenticated or getattr(user.role, 'role', None) != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            instance = Account.objects.get(pk = pk)
        except Account.DoesNotExist:
            return Response({'detail': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'detail': 'Admin deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
