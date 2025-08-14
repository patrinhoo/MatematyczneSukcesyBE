from django.db import models
from django.conf import settings

from apps.tasks.domain.enums.tasks import (
    TaskType,
    TaskDifficulty,
    EducationLevel,
)


class TaskOrm(models.Model):
    category = models.ForeignKey(
        "core.CategoryOrm",
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
    )
    education_level = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
    )
    type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.OPEN,
    )
    difficulty = models.CharField(
        max_length=20,
        choices=TaskDifficulty.choices,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks_created",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Zadanie #{self.id} - {self.category.name}"
