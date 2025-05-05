from django.db import models


class TaskType(models.TextChoices):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class TaskDifficulty(models.TextChoices):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class EducationLevel(models.TextChoices):
    MATURA_BASIC = "MATURA_BASIC"
    MATURA_EXTENDED = "MATURA_EXTENDED"
