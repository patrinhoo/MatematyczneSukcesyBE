from django.contrib.auth.models import (
    BaseUserManager,
)
from apps.users.domain.enums.users import UserRole


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
