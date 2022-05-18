from json import loads

import aiogram.utils.markdown as md
import requests
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ParseMode
from aiogram.utils.callback_data import CallbackData

from apps.telegram_bot.constants import API_LINK_FOR_TELEGRAM_BOTS
from apps.telegram_bot.management.loaders.telegram_manual_bot_loader import dp
from apps.telegram_bot.services import get_jwt_token


@dp.message_handler(Command("get_accounts"))
@dp.message_handler(text="Ваши аккаунты")
async def cmd_get_accounts(message: types.Message):
    token = get_jwt_token(message.from_user.id)
    request_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    path = "telethon/accounts/"
    url = API_LINK_FOR_TELEGRAM_BOTS + path

    response = requests.get(url, headers=request_headers)

    if not response.status_code == 200:
        await message.reply("Внутренняя ошибка сервера, попробуйте позже")
        return

    content = loads(response.text)

    if not content:
        await message.reply("У вас нет добавленных аккаунтов")
        return

    for account in content:
        keyboard = types.InlineKeyboardMarkup()
        activate_button = types.InlineKeyboardButton(
            text="Активировать",
            callback_data=cb.new(action="activate", id=account["id"]),
        )
        if not account["is_active"]:
            keyboard.add(activate_button)
        delete_button = types.InlineKeyboardButton(
            text="Удалить", callback_data=cb.new(action="delete", id=account["id"])
        )
        if account["is_permanent_banned"]:
            keyboard.add(delete_button)
        await message.reply(
            md.text(
                md.text("Api id: ", md.bold(account["api_id"])),
                md.text("Api hash: ", md.bold(account["api_hash"])),
                md.text("Номер телефона: ", account["phone_number"]),
                md.text(
                    "Инициализирован?",
                    md.bold("Да") if account["is_initialized"] else md.bold("Нет"),
                ),
                md.text(
                    "Занят работой?",
                    md.bold("Да") if account["is_busy"] else md.bold("Нет"),
                ),
                md.text(
                    "Активен?",
                    md.bold("Да") if account["is_active"] else md.bold("Нет"),
                ),
                md.text(
                    "Дата последней деактивации:",
                    md.bold(account["date_of_last_deactivate"]),
                ),
                md.text(
                    "Причина последней деактивации:",
                    md.bold(account["reason_of_last_deactivate"]),
                ),
                sep="\n",
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard,
        )


cb = CallbackData("post", "action", "id")


@dp.callback_query_handler(cb.filter())
async def callbacks(call: types.CallbackQuery, callback_data: dict):
    if callback_data["action"] == "activate":
        id = callback_data["id"]
        token = get_jwt_token(call.message.chat.id)
        request_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        path = f"telethon/accounts/{id}/activate/"
        url = API_LINK_FOR_TELEGRAM_BOTS + path
        response = requests.get(url, headers=request_headers)

        if not response.status_code == 200:
            await call.answer(text="Произошла ошибка, попробуйте позже")
            return
        await call.answer(text="Аккаунт успешно активирован, обновите список")
    elif callback_data["action"] == "delete":
        id = callback_data["id"]
        token = get_jwt_token(call.message.chat.id)
        request_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        path = f"telethon/accounts/{id}/"
        url = API_LINK_FOR_TELEGRAM_BOTS + path
        response = requests.delete(url, headers=request_headers)

        if not response.status_code == 204:
            await call.answer(text="Произошла ошибка, попробуйте позже")
            return
        await call.answer(text="Аккаунт успешно удален, обновите список")
    else:
        return
