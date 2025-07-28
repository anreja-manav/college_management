from django.shortcuts import render
from .models import Class, Students
from .serializers import ClassSerializer, StudentsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class StudentAPI(APIView):
    
    def get(self, request):
        obj = Students.objects.all()
        serializer = StudentsSerializer(obj, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        data = request.data
        serializer = StudentsSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
    def put(self, request):
        data = request.data
        serializer = StudentsSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
    def patch(self, request):
        data = request.data
        obj = Students.objects.get(id = data['id'])
        serializer = StudentsSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
    def delete(self, request):
        data = request.data
        obj = Students.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'Student Deleted'})

