from django.utils import timezone
from rest_framework import serializers
from students.models import Student


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        help_text='Пароль. Передаётся только явно при создании/смене пароля.',
    )

    class Meta:
        model = Student
        fields = [
            'id',
            'username', 'first_name', 'last_name', 'email', 'password',
            'phone', 'birth_date', 'registration_date',
            'is_active', 'date_joined',
        ]
        read_only_fields = ['id', 'registration_date', 'date_joined', 'is_active']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate_birth_date(self, value):
        if value and value > timezone.localdate():
            raise serializers.ValidationError('Дата рождения не может быть в будущем.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        student = Student(**validated_data)
        if password:
            student.set_password(password)
        student.save()
        return student

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance