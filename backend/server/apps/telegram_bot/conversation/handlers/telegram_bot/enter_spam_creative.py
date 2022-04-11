from telegram import Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import SHOW_DATA, State


def enter_spam_creative(update: Update, context: CallbackContext) -> str:
    """ввести данные для продвижения"""
    State.invite["days"] = update.callback_query.data
    text = "Укажите рекламный креатив, для продвижения рассылкой! !"
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)
    return SHOW_DATA
