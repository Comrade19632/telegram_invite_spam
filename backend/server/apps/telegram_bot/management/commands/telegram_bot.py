from django.conf import settings
from django.core.management.base import BaseCommand

from telegram.ext import Updater

from apps.telegram_bot.services.conversation_handlers import get_menu_conv_handler


class Command(BaseCommand):
    help = "Running telegram bot"

    def handle(self, *args, **kwargs):
        return
        # """
        # This is a echo bot.
        # It echoes any incoming text messages.
        # """

        # import logging

        # from aiogram import Bot, Dispatcher, executor, types

        # API_TOKEN = '1683215049:AAG7mWcDTpXwBMiJ3UZMdOPC3Zjf6w6poMY'

        # # Configure logging
        # logging.basicConfig(level=logging.INFO)

        # # Initialize bot and dispatcher
        # bot = Bot(token=API_TOKEN)
        # dp = Dispatcher(bot)


        # @dp.message_handler(commands=['start', 'help'])
        # async def send_welcome(message: types.Message):
        #     """
        #     This handler will be called when user sends `/start` or `/help` command
        #     """
        #     await message.reply("Hi!\nI'm EwchoBot!\nPowered by aiogram.")


        # @dp.message_handler(regexp='(^cat[s]?$|puss)')
        # async def cats(message: types.Message):
        #     with open('data/cats.jpg', 'rb') as photo:
        #         '''
        #         # Old fashioned way:
        #         await bot.send_photo(
        #             message.chat.id,
        #             photo,
        #             caption='Cats are here 😺',
        #             reply_to_message_id=message.message_id,
        #         )
        #         '''

        #         await message.reply_photo(photo, caption='Cats are here 😺')


        # @dp.message_handler()
        # async def echo(message: types.Message):
        #     # old style:
        #     # await bot.send_message(message.chat.id, message.text)

        #     await message.answer(message.text)


        # executor.start_polling(dp, skip_updates=True)