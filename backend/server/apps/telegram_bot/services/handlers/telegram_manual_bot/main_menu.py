from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

from apps.telegram_bot.management.loaders.telegram_manual_bot_loader import dp

base_menu_keyboard = ReplyKeyboardMarkup(
  keyboard=[
    [
      KeyboardButton(text="Добавить аккаунт"),
      KeyboardButton(text="Ваши аккаунты"),
    ],
    [
      KeyboardButton(text="Рассылка"),
      KeyboardButton(text="Приглашения"),
    ],
    [
      KeyboardButton(text="Парсинг аккаунтов"),
      KeyboardButton(text="Выход"),
    ],
  ],
  resize_keyboard=True
)

@dp.message_handler(Command("start"))
async def show_menu(message: types.Message):
  await message.answer("Варианты работы с ботом", reply_markup=base_menu_keyboard)
