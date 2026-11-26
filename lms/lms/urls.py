from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView,SpectacularSwaggerView,)

from courses.urls import courses_router
from enrollments.urls import enrollments_router
from students.urls import students_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', include(students_router.urls)),
    path('api/', include(courses_router.urls)),
    path('api/', include(enrollments_router.urls)),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]