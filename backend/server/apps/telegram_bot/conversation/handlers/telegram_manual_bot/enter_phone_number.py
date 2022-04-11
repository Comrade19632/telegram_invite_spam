from telegram import Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import DATA_VALIDATION, State


def enter_phone_number(update: Update, context: CallbackContext) -> str:
    """Введите номер телефона от Вашего ТГ аккаунта"""
    #сохраняем данные предидущего ввода
    State.tg_data["hash_id"] = update.message.text
    text = "Укажите номер тетефона от Вашего ТГ аккаунта"
    update.message.reply_text(text=text)
    return DATA_VALIDATION
