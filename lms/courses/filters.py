import django_filters

from courses.models import Course


class CourseFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')
    price = django_filters.RangeFilter()

    class Meta:
        model = Course
        fields = ['status', 'price']