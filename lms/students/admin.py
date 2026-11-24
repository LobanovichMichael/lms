from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from students.models import Student


@admin.register(Student)
class StudentAdmin(UserAdmin):
    ordering = ('username',)

    readonly_fields = ('registration_date',)
    fieldsets = (
        ('Credentials', {'fields': ('username', 'password')}),
        ('User info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'registration_date')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')