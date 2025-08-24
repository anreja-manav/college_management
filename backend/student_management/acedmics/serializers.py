from rest_framework import serializers
from .models import Result, Courses

class ResultSerializer(serializers.ModelSerializer):
    total_marks = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = '__all__'

    def get_total_marks(self, obj):
        return obj.total_marks()

    def get_percentage(self, obj):
        return obj.percentage()

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'