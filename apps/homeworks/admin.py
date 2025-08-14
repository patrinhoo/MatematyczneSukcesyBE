from django.contrib import admin

from apps.homeworks.models.homework_orm import HomeworkOrm
from apps.homeworks.models.homework_task_orm import HomeworkTaskOrm


admin.site.register(HomeworkOrm)
admin.site.register(HomeworkTaskOrm)
