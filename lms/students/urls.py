from rest_framework.routers import DefaultRouter
from students.views import StudentViewSet

students_router = DefaultRouter()
students_router.register('students', StudentViewSet, basename='student')


