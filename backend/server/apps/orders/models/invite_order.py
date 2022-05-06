from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    PROTECT,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
)

from apps.telethon_app.models import TelethonAccount
from common.models import ActiveModel, TimeStampedModel


class InviteOrder(TimeStampedModel, ActiveModel):
    telethon_accounts = ManyToManyField(
        TelethonAccount, blank=True, related_name="orders"
    )
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        blank=True,
        null=True,
    )
    target_chat_link = CharField(max_length=128, verbose_name="target chat link")
    donor_chat_link = CharField(max_length=128, verbose_name="donor chat link")
    affected_users = ArrayField(
        CharField(max_length=128), default=list, null=True, blank=True
    )
    in_progress = BooleanField(
        verbose_name="В процессе выполнения?",
        default=False,
        db_index=True,
    )
    was_online_user_delta = DateTimeField(blank=True, null=True)
    get_recently_online_users = BooleanField(
        default=False,
        db_index=True,
    )

    def __str__(self):
        if not self.is_active:
            return f"!НЕАКТИВЕН! {self.donor_chat_link} -> {self.target_chat_link}"
        return f"{self.donor_chat_link} -> {self.target_chat_link}"
