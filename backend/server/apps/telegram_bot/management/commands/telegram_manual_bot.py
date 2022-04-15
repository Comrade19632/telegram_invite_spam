import logging

from django.conf import settings
from django.core.management.base import BaseCommand

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor


class Command(BaseCommand):
    help = "Running manual telegram bot"

    def handle(self, *args, **kwargs):
        """инициализация бота"""
        from aiogram import executor
        from apps.telegram_bot.services.handlers.telegram_manual_bot import dp

        executor.start_polling(dp, on_startup=self.on_startup)

    async def on_startup(self, dp):
        """базовые действия при старте"""

        # установка фильтров и мидлварей
        # from apps.telegram_bot.conversation.filters import filters
        # from apps.telegram_bot.management.middlewares import middlewares
        # filters.setup(dp)
        # middlewares.setup(dp)

        # команды в боте
        await dp.bot.set_my_commands(
            [
                types.BotCommand("add_account", "Добавить аккаунт в бота"),
                types.BotCommand("get_accounts", "Посмотреть все мои аккаунты"),
                types.BotCommand("start", "Начать работу"),
                types.BotCommand("invite", "Нчать инвайтинг"),
                types.BotCommand("cancel", "Закончить работу"),
            ]
        )
