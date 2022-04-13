from django.conf import settings
from django.db.models import PROTECT, BooleanField, CharField, ForeignKey

from phonenumber_field.modelfields import PhoneNumberField

from common.models import ActiveModel, TimeStampedModel


class TelethonAccount(TimeStampedModel, ActiveModel):
    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        blank=True,
        null=True,
    )
    api_id = CharField(max_length=128, verbose_name="Telegram api id")
    api_hash = CharField(max_length=128, verbose_name="Telegram api hash")
    phone_number = PhoneNumberField(
        verbose_name="Номер телефона",
    )
    is_initialized = BooleanField(
        verbose_name="Инициализирован?",
        default=False,
        db_index=True,
    )

    def __str__(self):
        if not self.is_active:
            return f"!НЕАКТИВЕН! {str(self.phone_number)}"
        if not self.is_initialized:
            return f"!НЕИНИЦИАЛИЗИРОВАН! {str(self.phone_number)}"
        return str(self.phone_number)
