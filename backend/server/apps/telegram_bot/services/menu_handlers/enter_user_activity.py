from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from apps.telegram_bot.services.step_variables import (
    CURRENT_MENU,
    EIGHT,
    FOUR,
    SHOW_DATA,
    SIX,
    SPAM_CREATIVE,
    SPAMMING,
    TWO,
    State,
)


def enter_user_activity(update: Update, context: CallbackContext) -> str:
    """Данные для продвижения"""
    State.invite["groups"] = update.message.text
    buttons = [
        [
            InlineKeyboardButton(text="2 дня", callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(text="4 дня", callback_data=str(FOUR)),
        ],
        [
            InlineKeyboardButton(text="6 дней", callback_data=str(SIX)),
        ],
        [
            InlineKeyboardButton(text="8 дней", callback_data=str(EIGHT)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    text = "Нажмите на кнопку! Которая указывает примерное время\nпоследней активности необходимых пользователей"
    update.message.reply_text(text=text, reply_markup=keyboard)

    user_data = context.user_data
    if user_data[CURRENT_MENU] == SPAMMING:
        return SPAM_CREATIVE

    return SHOW_DATA
