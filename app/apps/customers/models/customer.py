from django.db.models import CharField, PositiveIntegerField

from phonenumber_field.modelfields import PhoneNumberField

from common.models import ActiveModel


class Customer(ActiveModel):
    first_name = CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    telegram_user_name = CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    telegram_chat_id = PositiveIntegerField(
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Номер телефона",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        if not self.is_active:
            return f"!НЕАКТИВЕН! {self.phone_number or self.telegram_chat_id}"
        return str(self.phone_number or self.telegram_chat_id)
