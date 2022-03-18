from django.conf import settings
from django.core.management.base import BaseCommand

from telegram.ext import Updater


class Command(BaseCommand):
    help = "Running telegram bot"

    def handle(self, *args, **kwargs):
        updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)

        # Start the Bot
        updater.start_polling()

        updater.idle()
