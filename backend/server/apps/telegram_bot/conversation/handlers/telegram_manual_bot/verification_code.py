from telegram import Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import CHECK_PASS, TG_DATA
from apps.orders.services import initialize_telethon_accounts
from apps.orders.models import TelethonAccount


def verification_code(update: Update, context: CallbackContext) -> str:
    """
    Отправка данных для аунтификации ТГ аккаунта,
    сохранения этих данных в БД,
    ввод пароля подтвеждения.
    """
    TelethonAccount.objects.create(
        api_id = context.user_data[TG_DATA]['id'],
        api_hash = context.user_data[TG_DATA]['hash_id'],
        phone_number = context.user_data[TG_DATA]['phone_number'],
        )
    initialize_telethon_accounts()
    

    text = "Сейчас в Ваш Телеграм аккаунт прийдет пароль подтвеждения"
    text += "\nВы должны его ввести сюда и нажать Enter"
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return CHECK_PASS