from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db.models import PROTECT, BooleanField, CharField, ForeignKey

from phonenumber_field.modelfields import PhoneNumberField

from common.models import ActiveModel, TimeStampedModel


class InviteOrder(TimeStampedModel, ActiveModel):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        blank=True,
        null=True,
    )
    target_chat_link = CharField(max_length=128, verbose_name="target chat link")
    donor_chat_link = CharField(max_length=128, verbose_name="donor chat link")
    affected_users = ArrayField(CharField(max_length=128))

    def __str__(self):
        if not self.is_active:
            return f"!НЕАКТИВЕН! {self.donor_chat_link} -> {self.target_chat_link}"
        return f"{self.donor_chat_link} -> {self.target_chat_link}"
