from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from courses.models import Course, CourseStatus
from courses.serializers import CourseSerializer
from enrollments.models import Enrollment, EnrollmentStatus
from students.serializers import StudentShortSerializer


class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.order_by('created', 'id')
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=request.method == 'PATCH')
        serializer.is_valid(raise_exception=True)
        new_price = request.data.get('price')
        if new_price and int(new_price) != instance.price:
            has_active = Enrollment.objects.filter(course=instance,status=EnrollmentStatus.ACTIVE,).exists()
            if has_active:
                raise ValidationError(
                    {'price': 'Невохможно изменить стоимость курса, на который есть активные записи.'}
                )
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == CourseStatus.ARCHIVED:
            raise ValidationError({'course': 'Невозможно повторно удалить курс'})

        if Enrollment.objects.filter(course=instance,status=EnrollmentStatus.ACTIVE,).exists():
            raise ValidationError({'course': 'Невозможно удалить курс, на котором есть активные записи.'})
        instance.status = CourseStatus.ARCHIVED
        instance.save(update_fields=['status'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        course = self.get_object()
        enrollments = Enrollment.objects.filter(course=course,status=EnrollmentStatus.ACTIVE,).select_related('student')
        students = [enr.student for enr in enrollments]
        return Response(StudentShortSerializer(students, many=True).data)