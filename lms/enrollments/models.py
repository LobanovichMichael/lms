from datetime import timezone

from django.db import models
from courses.models import Course
from students.models import Student


class EnrollmentStatus(models.TextChoices):
    ACTIVE = 'active', 'Активна'
    CANCELLED = 'cancelled', 'Отменена'


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата записи')
    status = models.CharField(max_length=20, choices=EnrollmentStatus.choices, default=EnrollmentStatus.ACTIVE,
                              verbose_name='Статус записи', )

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course',
            ),
            models.CheckConstraint(
                condition=models.Q(status__in=EnrollmentStatus.values),
                name='enrollment_status_valid',
            ),
        ]
