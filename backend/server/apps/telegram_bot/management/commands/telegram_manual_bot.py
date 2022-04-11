from django.conf import settings
from django.core.management.base import BaseCommand

from telegram.ext import Updater

from apps.telegram_bot.conversation.conversation_handlers.telegram_manual_bot import enter_tg_data_conv_handler


class Command(BaseCommand):
    help = "Running manual telegram bot"

    def handle(self, *args, **kwargs):
        updater = Updater(settings.TELEGRAM_MANUAL_BOT_TOKEN, use_context=True)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher
        dispatcher.add_handler(enter_tg_data_conv_handler())

        # Start the Bot
        updater.start_polling()

        updater.idle()
