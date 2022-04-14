from django.core.management.base import BaseCommand
from apps.telegram_bot.management.utils import set_default_commands


class Command(BaseCommand):
    help = "Running manual telegram bot"

    def handle(self, *args, **kwargs):
        """инициализация бота"""
        from aiogram import executor
        from apps.telegram_bot.conversation.handlers import dp

        executor.start_polling(dp, on_startup=self.on_startup)
       
    async def on_startup(self, dp):
        """базовые действия при старте"""

        #установка фильтров и мидлварей
        # from apps.telegram_bot.conversation.filters import filters
        # from apps.telegram_bot.management.middlewares import middlewares
        # filters.setup(dp)
        # middlewares.setup(dp)

        #команды в боте 
        await set_default_commands(dp)

       
        
    
        
        

        

