from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView,)
from rest_framework.routers import DefaultRouter

from enrollments.views import EnrollmentViewSet
from students.urls import students_router
from courses.views import CourseViewSet


courses_router = DefaultRouter()
courses_router.register('courses', CourseViewSet, basename='course')

enrollments_router = DefaultRouter()
enrollments_router.register('enrollments', EnrollmentViewSet, basename='enrollment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', include(students_router.urls)),
    path('api/', include(courses_router.urls)),
    path('api/', include(enrollments_router.urls)),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]