from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class UserGender(models.TextChoices):
    MALE = "MALE"
    FEMALE = "FEMALE"
