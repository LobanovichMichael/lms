from django.utils import timezone
from rest_framework import serializers
from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['created']

    def validate_price(self, value):
        if value and value < 0:
            raise serializers.ValidationError('Стоимость курса не может быть отрицательной')
        return value

    def validate_created(self, value):
        if value and value > timezone.localdate():
            raise serializers.ValidationError('Дата создания не может быть в будущем.')
        return value

    def validate_edited(self, value):
        if value and value > timezone.localdate():
            raise serializers.ValidationError('Дата изменения не может быть в будущем.')
        return value


class CourseShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'price', 'status')
