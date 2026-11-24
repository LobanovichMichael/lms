from django.contrib import admin

from enrollments.models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'created', 'status')
    list_filter = ('status', 'course', 'created')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'course__name')
    ordering = ('-created',)
    readonly_fields = ('created',)
    fields = ('student', 'course', 'status')