from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from apps.telegram_bot.services.step_variables import (
    CONFIRM,
    CURRENT_MENU,
    END,
    INVITE,
    SELECTING_MENU,
    SPAMMING,
    START_OVER,
    State,
)


def show_data(update: Update, context: CallbackContext) -> str:
    """Вывод данных на экран"""
    buttons = [
        [InlineKeyboardButton(text="Подтвердить", callback_data=str(CONFIRM))],
        [InlineKeyboardButton(text="Выход", callback_data=str(END))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    user_data = context.user_data
    if user_data[CURRENT_MENU] == SPAMMING:
        State.invite["creative"] = update.message.text
        user_data[user_data[CURRENT_MENU]] = State.invite
        text = ""
        if user_data.get(SPAMMING):
            text += (
                f"Группа для продвижения рассылки : \n{user_data[SPAMMING]['group']}"
            )
            text += (
                f"\n\nГруппы доноры для рассылки : \n{user_data[SPAMMING]['groups']}"
            )
            text += f"\n\nАктивность пользователей для рассылки : \n{user_data[SPAMMING]['days']}"
            text += f"\n\nРекламный креатив для продвижения рассылкой : \n{user_data[SPAMMING]['creative']}"
            text += "\n==========================================\n\n"
        else:
            text += "\n В разделе продвижения приглашениями Данные отсутствуют"

        update.message.reply_text(text=text, reply_markup=keyboard)

    if user_data[CURRENT_MENU] == INVITE:
        State.invite["days"] = update.callback_query.data
        user_data[user_data[CURRENT_MENU]] = State.invite
        text = ""
        if user_data.get(INVITE):
            text += (
                f"Группа для продвижения приглашениями : \n{user_data[INVITE]['group']}"
            )
            text += (
                f"\n\nГруппы доноры для приглашений : \n{user_data[INVITE]['groups']}"
            )
            text += f"\n\nАктивность пользователей для приглашений : \n{user_data[INVITE]['days']}"
            text += "\n==========================================\n\n"
        else:
            text += "\n В разделе продвижения приглашениями Данные отсутствуют"

        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    user_data[START_OVER] = True
    return SELECTING_MENU
