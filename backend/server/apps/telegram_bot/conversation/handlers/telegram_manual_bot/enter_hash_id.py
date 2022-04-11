from telegram import Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import ENTER_PHONE_NUMBER, State


def enter_hash_id(update: Update, context: CallbackContext) -> str:
    """Введите hash_id от Вашего ТГ аккаунта"""
    #сохраняем данные предидущего ввода
    State.tg_data["id"] = update.message.text
    text = "Укажите hash_id от Вашего ТГ аккаунта"
    update.message.reply_text(text=text)
    return ENTER_PHONE_NUMBER
