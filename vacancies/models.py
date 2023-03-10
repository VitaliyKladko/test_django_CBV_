from django.db import models


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

    def __str__(self):
        return self.slug
