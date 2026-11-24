from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser

from courses.models import Course
from courses.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD студентов платформы.

    - GET  /api/students/             — списком
    - POST /api/students/             — создать студента
    - GET  /api/students/{id}/        — один студент
    - PUT/PATCH /api/students/{id}/   — обновление
    - DELETE /api/students/{id}/      — удаление
    """
    queryset = Course.objects.order_by('created', 'id')
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]
