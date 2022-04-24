from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db.models import PROTECT, BooleanField, CharField, ForeignKey

from phonenumber_field.modelfields import PhoneNumberField

from common.models import ActiveModel, TimeStampedModel


class SpamOrder(TimeStampedModel, ActiveModel):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        blank=True,
        null=True,
    )
    spam_message = CharField(max_length=1000, verbose_name="spam message")
    donor_chat_link = CharField(max_length=128, verbose_name="donor chat link")
    affected_users = ArrayField(CharField(max_length=128), default=list)
    in_progress = BooleanField(
        verbose_name="В процессе выполнения?",
        default=False,
        db_index=True,
    )

    def __str__(self):
        if not self.is_active:
            return f"!НЕАКТИВЕН! {self.spam_message} -> {self.donor_chat_link}"
        return f"{self.spam_message} -> {self.donor_chat_link}"
