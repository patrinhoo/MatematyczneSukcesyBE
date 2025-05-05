from django.contrib import admin

from homeworks import models


admin.site.register(models.Homework)
admin.site.register(models.HomeworkTask)
