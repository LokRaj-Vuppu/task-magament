import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class TimeStampsForModels(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, TimeStampsForModels):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS: list[str] = []

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.email}"
