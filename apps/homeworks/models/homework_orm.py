from django.db import models
from django.conf import settings

from apps.homeworks.domain.enums.homeworks import HomeworkStatus


class HomeworkOrm(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=HomeworkStatus.choices, default=HomeworkStatus.DRAFT
    )

    due_date = models.DateTimeField(help_text="Deadline oddania pracy domowej.")
    ready_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Data oznaczenia zadania jako do zrobienia.",
    )
    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Data przesłania rozwiązania przez ucznia.",
    )
    checked_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Data sprawdzenia rozwiązania przez nauczyciela.",
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
        return f"Praca domowa: {self.title} ({self.assigned_to.given_name} {self.assigned_to.last_name})"
