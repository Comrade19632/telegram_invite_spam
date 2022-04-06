from telegram import Update
from telegram.ext import CallbackContext

from apps.telegram_bot.services.step_variables import END


def end(update: Update, context: CallbackContext) -> int:
    """Завершить разговор с помощью InlineKeyboardButton."""
    update.callback_query.answer()
    text = "Заходи еще =)"
    update.callback_query.edit_message_text(text=text)

    return END
