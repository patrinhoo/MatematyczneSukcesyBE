from django.contrib import admin

from apps.tasks import models


admin.site.register(models.Task)
admin.site.register(models.TaskBlock)
admin.site.register(models.ClosedAnswer)
