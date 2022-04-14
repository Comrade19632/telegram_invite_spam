from cgitb import text
from email.message import Message
from aiogram import types
from apps.telegram_bot.management.commands.loader import dp
from aiogram.dispatcher.filters.builtin import CommandStart

@dp.message_handler(CommandStart())
async def start(message: types.Message):
  """Принимает команду страрт"""  
  chat_id = message.from_user.id
  text = f"Привет! {message.from_user.id} ТЫ подключился к боту!"
  await dp.bot.send_message(chat_id, text)
