from django.db import models

from apps.tasks.domain.enums.tasks import TaskBlockType


class TaskBlockOrm(models.Model):
    task = models.ForeignKey(
        "tasks.TaskOrm",
        on_delete=models.CASCADE,
        related_name="blocks",
    )
    order = models.PositiveIntegerField()
    type = models.CharField(
        max_length=20,
        choices=TaskBlockType,
    )
    inline = models.BooleanField(default=False)

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
