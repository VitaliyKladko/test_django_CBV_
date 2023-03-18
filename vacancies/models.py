from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=20)

    # дополнительная информация класс Мета (пример перевода django админки)
    class Meta:
        verbose_name = 'Навык'  # название модели
        verbose_name_plural = 'Навыки'  # название модели во множественном числе

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    # список tuple - где первое значение лежит в базе, второе отображается в админке приложения
    # STATUS - это enum
    STATUS = [
        ('draft', 'Черновик'),
        ('open', 'Открытая'),
        ('closed', 'Закрытая')
    ]

    slug = models.SlugField(max_length=50)
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=6, choices=STATUS, default='draft')
    created = models.DateField(auto_now_add=True)
    # on_delete говорит что делать, если родительская запись будет удалена on_delete=models.CASCADE - каскадное удаление
    # всех вакансий конкретного User
    # null=True -user может быть пустым
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(Skill)

    class Meta:
        verbose_name = 'Вакансия'  # название модели
        verbose_name_plural = 'Вакансии'  # название модели во множественном числе (отображаются в админке)
        # ordering = ['-text']  #сортировка по модели

    def __str__(self):
        return self.slug
