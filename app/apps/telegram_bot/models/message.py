from django.db.models import CharField, PositiveIntegerField, TextField

from common.models import TimeStampedModel


class Message(TimeStampedModel):
    chat_id = CharField(
        max_length=255,
    )
    text = TextField()
    message_id = CharField(max_length=20, blank=True, null=True)
    my_order = PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ["my_order"]
        verbose_name = "Telegram сообщение"
        verbose_name_plural = "Telegram сообщения"

    def __str__(self):
        if len(self.text) > 20:
            return f"{self.text[:20]}..."
        else:
            return f"{self.text}"
