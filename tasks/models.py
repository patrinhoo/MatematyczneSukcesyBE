from django.db import models
from django.conf import settings

from core import models as core_models
from tasks.domain.enums.tasks import (
    TaskType,
    TaskDifficulty,
    EducationLevel,
    TaskBlockType,
    ClosedAnswerType,
)


class Task(models.Model):
    category = models.ForeignKey(
        core_models.Category,
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


class TaskBlock(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="blocks",
    )
    order = models.PositiveIntegerField()
    type = models.CharField(
        max_length=20,
        choices=TaskBlockType,
    )

    # Tylko jedno z tych pól będzie wypełnione, w zależności od typu
    content = models.TextField(
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="task_blocks/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Zadanie #{self.task.pk} - Blok #{self.pk}"


# TODO: TaskHint i TaskHintBlock (podpowiedź do zadania do zaimplementowania później)


class ClosedAnswer(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="closed_answers",
    )
    type = models.CharField(
        max_length=20,
        choices=ClosedAnswerType,
    )
    order = models.PositiveIntegerField()
    is_correct = models.BooleanField(default=False)

    # Tylko jedno z tych pól będzie wypełnione, w zależności od typu
    content = models.TextField(
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="closed_answers/",
        blank=True,
        null=True,
    )
