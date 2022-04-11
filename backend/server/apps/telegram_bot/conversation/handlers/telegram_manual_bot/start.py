from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import ENTER_ID, START_OVER


def start(update: Update, context: CallbackContext) -> str:
    """Начало дилога с ботом с ручным вводом данных ТГ акк"""
    text = "Далее Вам понадобится ввести данные Вашего ТГ аккаунта!"
    text += "\n\nid, hash_id и номер телефона на который зарегестирован Ваш ТГ"
    text += "\n\nС помощью этого аккаунта будет происходить парсинг, рассылка или приглашения"
    text += "\n\n\nКомманда /stop, для остановки бота"
    text += "\nКомманда /start, для запуска бота"
    button = InlineKeyboardButton(text="Продоллжить", callback_data=str(ENTER_ID))
    
    keyboard = InlineKeyboardMarkup.from_button(button)

    # Если мы начинаем сначала, то нам не нужно отправлять новое сообщение
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        update.message.reply_text(text=text, reply_markup=keyboard)

    return ENTER_ID
