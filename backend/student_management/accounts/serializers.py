from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Account, Roles, TeacherProfile, StudentProfile
from acedmics.models import Courses, Semesters

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['subject_specialization', 'qualification', 'experience_years', 'bio', 'profile_pic']

class StudentProfileSerializer(serializers.ModelSerializer):
    course_enrolled = serializers.SlugRelatedField(
        slug_field='course_name',
        queryset=Courses.objects.all()
    )
    semester = serializers.SlugRelatedField(
        slug_field='semester',
        queryset=Semesters.objects.all()
    )

    class Meta:
        model = StudentProfile
        fields = [
            'picture', 'course_enrolled', 'semester', 'roll_no',
            'father_name', 'father_occupation', 'father_phone',
            'mother_name', 'mother_occupation', 'mother_phone'
        ]
        validators = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self, 'partial', False):
            for field in ['course_enrolled', 'semester', 'roll_no']:
                self.fields[field].required = False

    def validate(self, attrs):
        roll_no = attrs.get('roll_no', getattr(self.instance, 'roll_no', None))
        course = attrs.get('course_enrolled', getattr(self.instance, 'course_enrolled', None))
        semester = attrs.get('semester', getattr(self.instance, 'semester', None))

        if roll_no and course and semester:
            qs = StudentProfile.objects.filter(
                roll_no=roll_no,
                course_enrolled=course,
                semester=semester
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError({
                    "non_field_errors": [
                        "A student with this roll number, course, and semester already exists."
                    ]
                })

        return attrs


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    role = serializers.SlugRelatedField(
        slug_field='role',
        queryset=Roles.objects.all()
    )
    student_profile = StudentProfileSerializer(required=False)
    teacher_profile = TeacherProfileSerializer(required=False)

    class Meta:
        model = Account
        fields = [
            'email', 'phone', 'password', 'role', 'id',
            'first_name', 'last_name', 'student_profile', 'teacher_profile'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({"password": "This field is required."})

        if self.instance is None and attrs.get('role') and attrs['role'].role == 'student':
            student_data = attrs.get('student_profile') or {}
            missing = []
            for field in ['course_enrolled', 'semester', 'roll_no']:
                if not student_data.get(field):
                    missing.append(field)
            if missing:
                raise serializers.ValidationError({
                    "student_profile": {
                        f: "This field is required for students." for f in missing
                    }
                })

        return super().validate(attrs)

    def create(self, validated_data):
        student_profile_data = validated_data.pop('student_profile', None)
        teacher_profile_data = validated_data.pop('teacher_profile', None)
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        account = super().create(validated_data)

        if account.role.role == 'student':
            StudentProfile.objects.create(user=account, **(student_profile_data or {}))
        elif account.role.role == 'teacher':
            TeacherProfile.objects.create(user=account, **(teacher_profile_data or {}))

        return account

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        student_profile_data = validated_data.pop('student_profile', None)
        teacher_profile_data = validated_data.pop('teacher_profile', None)

        if password:
            instance.password = make_password(password)

        account = super().update(instance, validated_data)

        if account.role.role == 'student' and student_profile_data:
            profile, _ = StudentProfile.objects.get_or_create(user=account)
            serializer = StudentProfileSerializer(
                profile,
                data=student_profile_data,
                partial=True,
                context=self.context
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        elif account.role.role == 'teacher' and teacher_profile_data:
            profile, _ = TeacherProfile.objects.get_or_create(user=account)
            serializer = TeacherProfileSerializer(
                profile,
                data=teacher_profile_data,
                partial=True,
                context=self.context
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
