from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from users.domain.enums.users import UserGender, UserRole


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(
        self,
        email: str,
        password=None,
        role: UserRole = UserRole.STUDENT,
        **extra_fields
    ):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(
            email=self.normalize_email(email).lower(), role=role, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password):
        """Create and return a new superuser."""
        user = self.create_user(email.lower(), password, UserRole.ADMIN)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
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
