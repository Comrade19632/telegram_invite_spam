import asyncio

from aiogram import Bot


async def send_message_to_user(token, telegram_id, text):
    bot = Bot(token)
    await bot.send_message(telegram_id, text=text)
    await bot.close()
