from telegram import Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import END


def stop(update: Update, context: CallbackContext) -> int:
    """Завершить разговор по команде."""
    update.message.reply_text("Приходи еще =)")

    return END
