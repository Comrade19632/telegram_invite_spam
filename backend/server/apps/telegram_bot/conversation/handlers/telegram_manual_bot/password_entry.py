from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import CHECK_PASS, TG_DATA


def password_entry(update: Update, context: CallbackContext) -> str:
    """
    Отправка данных для аунтификации ТГ аккаунта,
    сохранения этих данных в БД,
    ввод пароля подтвеждения.
    """
    """Данные для отправки хранятся здесь:
    context.user_data[TG_DATA]['id']
    context.user_data[TG_DATA]['hash_id']
    context.user_data[TG_DATA]['phone_number']
    """
    text = "Сейчас в Ваш Телеграм аккаунт прийдет пароль подтвеждения"
    text += "\nВы должны его ввести сюда и нажать Enter"
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return CHECK_PASS