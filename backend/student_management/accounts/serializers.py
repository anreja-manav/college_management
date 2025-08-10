from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Account, Roles


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required = False)
    role = serializers.SlugRelatedField(
        slug_field='role',
        queryset=Roles.objects.all()
    )

    class Meta:
        model = Account
        fields = ['email', 'phone', 'password', 'role', 'id', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({"password": "This field is required."})
        return super().validate(attrs)
    

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
