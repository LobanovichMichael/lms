from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet

courses_router = DefaultRouter()
courses_router.register('courses', CourseViewSet, basename='course')
