from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import AdminProfile

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AdminProfile
        fields = ['id', 'email', 'name', 'phone', 'password']
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()