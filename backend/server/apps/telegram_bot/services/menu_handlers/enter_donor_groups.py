from telegram import Update
from telegram.ext import CallbackContext

from apps.telegram_bot.services.step_variables import USER_ACTIVITY, State


def enter_donor_groups(update: Update, context: CallbackContext) -> str:
    """ввести данные для продвижения"""
    State.invite["group"] = update.message.text
    text = "Укажите группы в которых будем брать пользователей\n(через запятую)! \nПример: group1, group2, group3"
    update.message.reply_text(text=text)
    return USER_ACTIVITY
