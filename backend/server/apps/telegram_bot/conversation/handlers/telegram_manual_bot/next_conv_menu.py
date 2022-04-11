from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from apps.telegram_bot.conversation.step_variables import NEXT_CONV


def next_conv_menu(update: Update, context: CallbackContext) -> str:
    """переход в другое меню диалогов"""
    text = "Далее Вам нужно будет выбрать, каким способом нужно будет продвигаться"
    button = InlineKeyboardButton(text="Продоллжить", callback_data=str(NEXT_CONV))
    keyboard = InlineKeyboardMarkup.from_button(button)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return NEXT_CONV
