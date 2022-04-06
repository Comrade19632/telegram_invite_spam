from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from apps.telegram_bot.services.step_variables import (
    ADD_DATA,
    CURRENT_MENU,
    PROMOTION_BY_SPAMMING,
    SPAMMING,
)


def promotion_with_spamming(update: Update, context: CallbackContext) -> str:
    """Продвигать свою группу инвайтингом."""
    user_data = context.user_data
    user_data[CURRENT_MENU] = SPAMMING
    text = "Нажмите на кнопку, для продолжения!"
    button = InlineKeyboardButton(text="Добавить данные", callback_data=str(ADD_DATA))
    keyboard = InlineKeyboardMarkup.from_button(button)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return PROMOTION_BY_SPAMMING
