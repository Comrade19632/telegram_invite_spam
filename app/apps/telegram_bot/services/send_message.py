from django.conf import settings

from sentry_sdk import capture_exception
from telegram import Bot, ParseMode

from ..models import Message


class SendMessage:
    def __init__(self, chat_id, message):
        self.bot = Bot(settings.TELEGRAM_BOT_TOKEN)
        self.chat_id = chat_id
        self.message = message

    def __call__(self):
        message = Message.objects.create(chat_id=self.chat_id, text=self.message)

        try:
            message_telegram_object = self.bot.send_message(
                chat_id=self.chat_id, text=self.message, parse_mode=ParseMode.MARKDOWN
            )
            message.message_id = message_telegram_object.message_id
            message.save()

        except BaseException as error:
            capture_exception(error)
