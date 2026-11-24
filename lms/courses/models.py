from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class CourseStatus(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    PUBLISHED = 'published', 'Опубликован'
    ARCHIVED = 'archived', 'Архивирован'

class Course(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Название курса')
    description = models.CharField(max_length=512, null=True, blank=True, verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Цена')
    status = models.CharField(max_length=20, choices=CourseStatus.choices, default=CourseStatus.DRAFT,
                              verbose_name='Статус курса', )
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор курса')
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания курса')
    edited = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=CourseStatus.values),
                name='course_status_valid',
            ),
        ]

    def __str__(self):
        return self.name
