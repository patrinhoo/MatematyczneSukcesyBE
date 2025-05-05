from django.db import models
from django.conf import settings

from tasks import models as tasks_models


class Homework(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    due_date = models.DateTimeField(help_text="Deadline oddania pracy domowej.")
    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Data przesłania rozwiązania przez ucznia.",
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="homeworks_assigned",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="homeworks_received",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Praca domowa: {self.title} ({self.assigned_to.username})"


class HomeworkTask(models.Model):
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="homework_tasks"
    )
    task = models.ForeignKey(
        tasks_models.Task, on_delete=models.CASCADE, related_name="homework_tasks"
    )

    solution_file = models.FileField(
        upload_to="homework_solutions/",
        blank=True,
        null=True,
        help_text="Przesłane rozwiązanie (skan, zdjęcie, PDF, itd.).",
    )
    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Data przesłania rozwiązania przez ucznia.",
    )
