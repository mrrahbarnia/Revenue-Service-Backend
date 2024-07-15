import uuid

from common.models import BaseModel
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.db import models


def default_security_stamp() -> str:
    return uuid.uuid4().hex


class BaseUserManager(BUM):
    def create_user(
        self,
        email: str,
        is_active: bool = True,
        is_staff: bool = False,
        password: str | None = None,
    ) -> "BaseUser":
        """Creating normal users with the given email and password."""
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            is_staff=is_staff,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str) -> "BaseUser":
        user = self.create_user(
            email=email,
            is_active=True,
            is_staff=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", unique=True)  # type: ignore

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # type: ignore

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email
