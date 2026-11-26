from rest_framework.routers import DefaultRouter
from enrollments.views import EnrollmentViewSet

enrollments_router = DefaultRouter()
enrollments_router.register('enrollments', EnrollmentViewSet, basename='enrollment')
