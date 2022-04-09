from django.conf import settings
from django.db.models import CASCADE, PROTECT, ForeignKey, PositiveSmallIntegerField, CharField
from phonenumber_field.modelfields import PhoneNumberField
from common.models import TimeStampedModel, ActiveModel



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