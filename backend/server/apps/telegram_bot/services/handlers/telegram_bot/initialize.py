import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from apps.telegram_bot.management.loaders.telegram_bot_loader import dp


class Form(StatesGroup):
    api_id = State()  # Will be represented in storage as 'Form:api_id'
    api_hash = State()  # Will be represented in storage as 'Form:api_hash'
    phone_number = State()  # Will be represented in storage as 'Form:phone_number'
    verification_code = State()  # Will be represented in storage as 'Form:phone_number'


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.api_id.set()

    await message.reply("Hi there! What's your api_id?")


# You can use state '*' if you need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply("Cancelled.", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.api_id)
async def process_api_id(message: types.Message, state: FSMContext):
    """
    Process user api_id
    """
    async with state.proxy() as data:
        data["api_id"] = message.text

    await Form.next()
    await message.reply("api hash?")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.api_hash)
async def process_api_hash(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(api_hash=int(message.text))

    await message.reply("What is your phone_number?")


@dp.message_handler(state=Form.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    """
    Process user api_id
    """
    async with state.proxy() as data:
        data["phone_number"] = message.text
        client = await TelegramClient(
            TELETHON_SESSIONS_FOLDER + data["phone_number"],
            data["api_id"],
            data["api_hash"],
        )
        result_send_code_request = await client.send_code_request(data["phone_number"])
        data["phone_code_hash"] = result_send_code_request.phone_code_hash

    await Form.next()
    await message.reply("verification code")


@dp.message_handler(state=Form.verification_code)
async def process_verification_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["verification_code"] = message.text

        client = await TelegramClient(
            TELETHON_SESSIONS_FOLDER + data["phone_number"],
            data["api_id"],
            data["api_hash"],
        )
        await client.connect()
        await client.sign_in(
            data["phone_number"],
            data["verification_code"],
            phone_code_hash=data["phone_code_hash"],
        )

        if client.is_user_authorized():
            await message.reply("you added new account")
        else:
            await message.reply("something went wrong")
    # Finish conversation
    await state.finish()
