from rest_framework import status, viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from enrollments.models import Enrollment, EnrollmentStatus
from enrollments.serializers import EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):

    queryset = Enrollment.objects.order_by('id')
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    filter_backends = [filters.SearchFilter]
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'course__name']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == EnrollmentStatus.CANCELLED:
            raise ValidationError(
                {'status': 'Запись уже отменена. Повторная отмена невозможна.'}
            )

        instance.status = EnrollmentStatus.CANCELLED
        instance.save(update_fields=['status'])

        return Response(status=status.HTTP_204_NO_CONTENT)