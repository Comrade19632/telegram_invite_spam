from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from apps.telegram_bot.services.step_variables import (
    END,
    SELECT_INVITE,
    SELECT_SPAMMING,
    SELECTING_MENU,
    START_OVER,
)


# Обратные вызовы разговора верхнего уровня
def start(update: Update, context: CallbackContext) -> str:
    """Выберите действие приглашения/рассылка или показать данные"""
    text = (
        "Вы можете выбрать продвижение приглашениями, продвижение рассылкой или посмотреть уже имеющиесявведенные данные"
        "\n\nЧто бы прервать разговор, просто введите: /stop."
    )

    buttons = [
        [
            InlineKeyboardButton(text="Приглашения", callback_data=str(SELECT_INVITE)),
            InlineKeyboardButton(text="Рассылка", callback_data=str(SELECT_SPAMMING)),
        ],
        [
            InlineKeyboardButton(text="Выход", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # Если мы начинаем сначала, то нам не нужно отправлять новое сообщение
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        update.message.reply_text(
            "Привет, я Telegram бот, и я помогу Вам продвигаться в Telegram"
        )
        update.message.reply_text(text=text, reply_markup=keyboard)

    return SELECTING_MENU
