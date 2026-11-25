from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from courses.models import Course
from courses.serializers import CourseSerializer
from enrollments.models import Enrollment, EnrollmentStatus


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