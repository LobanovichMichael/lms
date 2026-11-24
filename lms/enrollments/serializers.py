from rest_framework import serializers
from enrollments.models import Enrollment, EnrollmentStatus
from courses.models import CourseStatus


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('id', 'student', 'course', 'created', 'status')
        read_only_fields = ('id', 'created')

    def validate_course(self, value):
        if value.status == CourseStatus.DRAFT:
            raise serializers.ValidationError('Невозможно записаться на курс, находящийся в разработке.')
        if value.status == CourseStatus.ARCHIVED:
            raise serializers.ValidationError('Невозможно записаться на заархивированный курс')
        return value
