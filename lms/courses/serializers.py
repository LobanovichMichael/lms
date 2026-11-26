from django.utils import timezone
from rest_framework import serializers
from courses.models import Course, CourseStatus


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

    def validate(self, attrs):
        new_status = attrs.get(
            'status',
            getattr(self.instance, 'status', None) if self.instance else None,
        )

        if new_status == CourseStatus.PUBLISHED:
            price = attrs.get('price')
            if price is None and self.instance:
                price = self.instance.price

            description = attrs.get('description')
            if description is None and self.instance:
                description = self.instance.description

            if price is None:
                raise serializers.ValidationError({
                    'price': 'Нельзя опубликовать курс без указания стоимости.'
                })

            if not (description and description.strip()):
                raise serializers.ValidationError({
                    'description': 'Нельзя опубликовать курс без описания.'
                })
        return attrs


class CourseShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'price', 'status')
