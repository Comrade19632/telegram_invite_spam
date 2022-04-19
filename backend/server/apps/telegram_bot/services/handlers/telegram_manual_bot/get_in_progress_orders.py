from json import loads

import aiogram.utils.markdown as md
import requests
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode
from aiogram.utils.callback_data import CallbackData

from apps.telegram_bot.constants import API_LINK_FOR_TELEGRAM_BOTS
from apps.telegram_bot.management.loaders.telegram_manual_bot_loader import dp
from apps.telegram_bot.services import get_jwt_token


@dp.message_handler(Command("get_in_progress_orders"))
@dp.message_handler(text="Ваши заказы в процессе")
async def cmd_get_in_progress_orders(message: types.Message):
    token = get_jwt_token(message.from_user.id)
    request_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    path = "orders/invite?in_progress=true"
    url = API_LINK_FOR_TELEGRAM_BOTS + path

    response = requests.get(url, headers=request_headers)

    if not response.status_code == 200:
        await message.reply("Внутренняя ошибка сервера, попробуйте позже")
        return

    content = loads(response.text)

    if not content:
        await message.reply("У вас нет заказов в процессе")
        return

    for order in content:
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
            text="Остановить", callback_data=cb.new(id=order["id"])
        )
        keyboard.add(button)
        await message.reply(
            md.text(
                md.text("Целевая группа: ", order["target_chat_link"]),
                md.text("Донор группа: ", order["donor_chat_link"]),
                sep="\n",
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard,
        )


cb = CallbackData("order_stop", "id")


@dp.callback_query_handler(cb.filter())
async def callbacks(call: types.CallbackQuery, callback_data: dict):
    id = callback_data["id"]
    token = get_jwt_token(call.message.chat.id)
    request_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    path = f"orders/invite/{id}/stop/"
    url = API_LINK_FOR_TELEGRAM_BOTS + path
    response = requests.get(url, headers=request_headers)

    if not response.status_code == 200:
        await call.answer(text="Произошла ошибка, попробуйте позже")
        return
    await call.answer(text="Заказ на инвайт успешно остановлен, обновите список")
