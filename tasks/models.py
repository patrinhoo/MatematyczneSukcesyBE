from django.db import models
from django.conf import settings

from core import models as core_models
from tasks.domain.enums.tasks import TaskType, TaskDifficulty, EducationLevel


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

    question_text = models.TextField()
    hint = models.TextField(
        blank=True,
        null=True,
        help_text="Opcjonalna podpowiedź dla ucznia.",
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


class ClosedAnswer(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="closed_answers"
    )
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
