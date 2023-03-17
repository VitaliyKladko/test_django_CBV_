from django.contrib import admin

from companies.models import Company

# регистрируем модель в админку
admin.site.register(Company)
