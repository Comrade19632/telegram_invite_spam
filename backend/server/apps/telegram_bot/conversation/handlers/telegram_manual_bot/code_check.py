from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import ADD_TG_ACC, START_PROMO, SELECTING_ACTION
from apps.orders.services import get_code


def code_check(update: Update, context: CallbackContext) -> str:
    """
    Отправляем пароль в скрипт для завершения аунтификации и создания сессии,
    Предлагаем выбор действий: Начать продвижение / Добавить еще аккаунт 
    """

    verification_code = update.message.text
    get_code(verification_code)
 
    buttons = [
        [InlineKeyboardButton(text="Начать продвижение", callback_data=str(START_PROMO))],
        [InlineKeyboardButton(text="Добавить еще аккаунт", callback_data=str(ADD_TG_ACC))],
            ]
    keyboard = InlineKeyboardMarkup(buttons)
    text = "Вы можете добавить еще один аккаунт или же начать продвижение"
    update.message.reply_text(text=text, reply_markup=keyboard)

    return SELECTING_ACTION
