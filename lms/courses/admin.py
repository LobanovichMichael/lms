from django.contrib import admin

from courses.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ('name','price','status','author','created','edited',)
    list_filter = ('status', 'author')
    search_fields = ('name', 'description')
    ordering = ('name', '-created',)
    readonly_fields = ('created', 'edited')

    fields = ('name','description', 'price','status','author',
              )
