from django.conf import settings
from django.core.management.base import BaseCommand




class Command(BaseCommand):
    help = "Running telegram bot"

    def handle(self, *args, **kwargs):
        pass
        # updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)

        # # Get the dispatcher to register handlers
        # # dispatcher = updater.dispatcher
        # # dispatcher.add_handler(promotion_conv_menu())

        # # Start the Bot
        # updater.start_polling()

        # updater.idle()
