from django.contrib import admin

from apps.tasks.models.closed_answer_orm import ClosedAnswerOrm
from apps.tasks.models.task_block_orm import TaskBlockOrm
from apps.tasks.models.task_orm import TaskOrm


admin.site.register(TaskOrm)
admin.site.register(TaskBlockOrm)
admin.site.register(ClosedAnswerOrm)
