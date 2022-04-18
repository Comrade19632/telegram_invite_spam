from django.conf import settings
from django.db.models import PROTECT, BooleanField, CharField, DateField, ForeignKey

from phonenumber_field.modelfields import PhoneNumberField

from common.models import ActiveModel, TimeStampedModel


class TelethonAccount(TimeStampedModel, ActiveModel):
    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        blank=True,
        null=True,
    )
    api_id = CharField(max_length=128, verbose_name="Telegram api id", unique=True)
    api_hash = CharField(max_length=128, verbose_name="Telegram api hash", unique=True)
    date_of_last_deactivate = DateField(
        blank=True, null=True, verbose_name="Дата последней деактивации"
    )
    reason_of_last_deactivate = CharField(
        blank=True,
        null=True,
        max_length=128,
        verbose_name="Причина последней деактивации",
    )
    phone_number = PhoneNumberField(verbose_name="Номер телефона", unique=True)
    is_initialized = BooleanField(
        verbose_name="Инициализирован?",
        default=False,
        db_index=True,
    )
    is_busy = BooleanField(
        verbose_name="Занят работой?",
        default=False,
        db_index=True,
    )

    def __str__(self):
        if not self.is_active:
            return f"!НЕАКТИВЕН! {str(self.phone_number)}"
        if not self.is_initialized:
            return f"!НЕИНИЦИАЛИЗИРОВАН! {str(self.phone_number)}"
        return str(self.phone_number)
