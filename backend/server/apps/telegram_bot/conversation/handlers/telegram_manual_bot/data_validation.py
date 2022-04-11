from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import (
    CONFIRM,
    State,
    CHANGE,
    TG_DATA,
    RESULT_OF_VALIDATION,
    START_OVER,
)


def data_validation(update: Update, context: CallbackContext) -> str:
    """Вывод данных на экран и проверка"""
    State.tg_data["phone_number"] = update.message.text
    context.user_data[TG_DATA] = State.tg_data
    text = (
                f"ID Вашего ТГ : \n{context.user_data[TG_DATA]['id']}"
            )
    text += (
                f"\n\nHASH_ID Вашего ТГ : \n{context.user_data[TG_DATA]['hash_id']}"
            )
    text += (
                f"\n\nНомер телефона Вашего ТГ : \n{context.user_data[TG_DATA]['phone_number']}"
            )
    buttons = [
        [InlineKeyboardButton(text="Исправить", callback_data=str(CHANGE))],
        [InlineKeyboardButton(text="Продолжить и вести код подтверждения", callback_data=str(CONFIRM))],
            ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=keyboard)
    context.user_data[START_OVER] = True
    return RESULT_OF_VALIDATION
