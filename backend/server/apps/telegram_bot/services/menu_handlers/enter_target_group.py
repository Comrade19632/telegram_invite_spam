from telegram import Update
from telegram.ext import CallbackContext

from apps.telegram_bot.services.step_variables import ENTER_DONOR_GROUPS


def enter_target_group(update: Update, context: CallbackContext) -> str:
    """ввести данные для продвижения"""
    text = "Укажите группу которую нужно продвигать !"
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return ENTER_DONOR_GROUPS
