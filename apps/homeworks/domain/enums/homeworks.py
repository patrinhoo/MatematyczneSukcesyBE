from django.db import models


class HomeworkStatus(models.TextChoices):
    DRAFT = "DRAFT"
    READY = "READY"
    SUBMITTED = "SUBMITTED"
    CHECKED = "CHECKED"
