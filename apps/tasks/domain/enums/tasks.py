from django.db import models


class TaskType(models.TextChoices):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class TaskDifficulty(models.TextChoices):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class TaskStatus(models.TextChoices):
    NEW = "NEW"
    WAITING_ACCEPT = "WAITING_ACCEPT"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class EducationLevel(models.TextChoices):
    MATURA_BASIC = "MATURA_BASIC"
    MATURA_EXTENDED = "MATURA_EXTENDED"


class TaskBlockType(models.TextChoices):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    LATEX = "LATEX"


class ClosedAnswerType(models.TextChoices):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    LATEX = "LATEX"
