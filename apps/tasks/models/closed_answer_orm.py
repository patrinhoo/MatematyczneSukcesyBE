from django.db import models

from apps.tasks.domain.enums.tasks import ClosedAnswerType


class ClosedAnswerOrm(models.Model):
    task = models.ForeignKey(
        "tasks.TaskOrm",
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
