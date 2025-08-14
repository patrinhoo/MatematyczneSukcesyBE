from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from apps.users.domain.enums.users import UserGender, UserRole
from apps.users.managers.user import UserManager


class UserOrm(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    given_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
    )
    gender = models.CharField(
        max_length=20,
        choices=UserGender.choices,
    )
    terms_confirmed = models.BooleanField(default=False)

    avatar = models.ImageField(
        upload_to="avatars/",
        default="assets/default_images/default_avatar.png",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def is_admin(self):
        return self.role == UserRole.ADMIN

    def is_student(self):
        return self.role == UserRole.STUDENT

    def is_teacher(self):
        return self.role == UserRole.TEACHER
