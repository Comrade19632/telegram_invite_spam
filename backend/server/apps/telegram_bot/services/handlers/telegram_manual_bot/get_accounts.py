from json import loads

import aiogram.utils.markdown as md
import requests
from aiogram import types
from aiogram.types import ParseMode

from apps.telegram_bot.constants import API_LINK_FOR_TELEGRAM_BOTS
from apps.telegram_bot.management.loaders.telegram_manual_bot_loader import dp
from apps.telegram_bot.services import get_jwt_token


@dp.message_handler(text="Ваши аккаунты")
async def cmd_add_account(message: types.Message):
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

    message_text = md.bold("Список добавленных аккаунтов:\n\n")

    for account in content:
        message_text += md.text("api id - ", md.bold(account["api_id"]), "\n")
        message_text += md.text("api hash - ", md.bold(account["api_hash"]), "\n")
        message_text += md.text(
            "Номер телефона - ", md.bold(account["phone_number"]), "\n"
        )
        message_text += md.text(
            "Инициализирован?",
            md.bold("Да") if account["is_initialized"] else md.bold("Нет"),
            "\n",
        )
        message_text += md.text(
            "Активен?", md.bold("Да") if account["is_active"] else md.bold("Нет"), "\n"
        )
        message_text += md.text("\n")

    await message.reply(
        md.text(
            message_text,
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
