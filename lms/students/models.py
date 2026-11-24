from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Student(User):
    phone = models.CharField(max_length=11, unique=True, verbose_name='Номер телефона',)
    birth_date = models.DateField(null=True,blank=True, verbose_name='Дата рождения',)
    registration_date = models.DateTimeField(default=timezone.now, editable=False, verbose_name='Дата регистрации студента',)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f'{self.first_name} {self.last_name} / {self.username}'