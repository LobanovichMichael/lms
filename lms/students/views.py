from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser

from students.models import Student
from students.serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    CRUD студентов платформы.

    - GET  /api/students/             — списком
    - POST /api/students/             — создать студента
    - GET  /api/students/{id}/        — один студент
    - PUT/PATCH /api/students/{id}/   — обновление
    - DELETE /api/students/{id}/      — удаление
    """
    queryset = Student.objects.order_by('id')
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    filter_backends = [filters.SearchFilter]
