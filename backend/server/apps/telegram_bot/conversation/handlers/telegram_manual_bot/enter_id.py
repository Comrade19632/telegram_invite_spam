from telegram import Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import ENTER_HASH_ID


def enter_id(update: Update, context: CallbackContext) -> str:
    """ввод ID телеграм аакаунта"""
    text = "Введите ID от Вашего Телеграм Аккаунта"
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)
    return ENTER_HASH_ID
