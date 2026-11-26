from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from courses.serializers import CourseShortSerializer
from enrollments.models import Enrollment, EnrollmentStatus
from students.models import Student
from students.serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.order_by('id')
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    filter_backends = [filters.SearchFilter]

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        student = self.get_object()
        enrollments = Enrollment.objects.filter(student=student,status=EnrollmentStatus.ACTIVE,).select_related('course')
        courses = [enr.course for enr in enrollments]
        return Response(CourseShortSerializer(courses, many=True).data)
