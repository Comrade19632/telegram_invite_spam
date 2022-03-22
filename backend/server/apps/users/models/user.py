from django.contrib.auth.models import AbstractUser
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    CheckConstraint,
    DateTimeField,
    EmailField,
    ForeignKey,
    Manager,
    Q,
    UniqueConstraint,
)

from .managers import UserManager


class User(AbstractUser):
    telegram_id = CharField(max_length=128, unique=True, verbose_name="Telegram id")
    username = CharField(
        max_length=128, blank=True, null=True, verbose_name="Telegram id"
    )
    USERNAME_FIELD = "telegram_id"

    objects = UserManager()
