import logging
import traceback

import aiogram.utils.markdown as md
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from telethon import TelegramClient, connection, events, sync
from telethon.errors.rpcerrorlist import (
    ApiIdInvalidError,
    FloodWaitError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
)

from apps.orders.constants import TELETHON_SESSIONS_FOLDER
from apps.telegram_bot.constants import API_LINK_FOR_TELEGRAM_BOTS
from apps.telegram_bot.management.loaders.telegram_manual_bot_loader import dp
from apps.telegram_bot.services import get_jwt_token
from aiogram.dispatcher.filters import Command


class Form(StatesGroup):
    api_id = State()  # Will be represented in storage as 'Form:api_id'
    api_hash = State()  # Will be represented in storage as 'Form:api_hash'
    phone_number = State()  # Will be represented in storage as 'Form:phone_number'
    verification_code = State()  # Will be represented in storage as 'Form:phone_number'


@dp.message_handler(Command("add_account"))
@dp.message_handler(text="Добавить аккаунт")
async def cmd_add_account(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.api_id.set()

    await message.reply("Введите api_id?")


# You can use state '*' if you need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="Выход", ignore_case=True), state="*")
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
    await message.reply("Программа отменена", reply_markup=types.ReplyKeyboardRemove())


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.api_id)
async def process_api_id_invalid(message: types.Message):
    return await message.reply(
        "api_id может содержать только цифры, введите настоящий api_id"
    )


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.api_id)
@dp.message_handler(state=Form.api_id)
async def process_api_id(message: types.Message, state: FSMContext):
    """
    Process user api_id
    """
    async with state.proxy() as data:
        data["api_id"] = message.text

    await Form.next()
    await message.reply("Введите api hash")


@dp.message_handler(state=Form.api_hash)
async def process_api_hash(message: types.Message, state: FSMContext):
    # Update state and data
    await state.update_data(api_hash=message.text)

    await Form.next()
    await message.reply("Введите номер телефона. Формат - +00000000000")


@dp.message_handler(state=Form.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    """
    Process user api_id
    """
    async with state.proxy() as data:
        data["phone_number"] = message.text
        client = TelegramClient(
            TELETHON_SESSIONS_FOLDER + data["phone_number"],
            data["api_id"],
            data["api_hash"],
        )
        try:
            await client.connect()
            result_send_code_request = await client.send_code_request(
                data["phone_number"]
            )
            data["phone_code_hash"] = result_send_code_request.phone_code_hash
            await client.disconnect()
        except ApiIdInvalidError:
            await client.disconnect()
            await message.reply("Неверные api id/hash, попробуйте снова")
            await state.finish()
            return
        except PhoneNumberInvalidError:
            await client.disconnect()
            await message.reply("Неверный номер телефона, попробуйте снова")
            await state.finish()
            return
        except FloodWaitError:
            await client.disconnect()
            await message.reply(
                "Слишком много запросов на получение кода, попробуйте снова через некоторое время, либо используйте другой аккаунт"
            )
            await state.finish()
            return
        except:
            traceback.print_exc()
            await message.reply("Что то пошло не так, попробуйте снова")
            await state.finish()
            return

    await Form.next()
    await message.reply("Введите код верификации, полученный в телеграме")


@dp.message_handler(state=Form.verification_code)
async def process_verification_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["verification_code"] = message.text

        client = TelegramClient(
            TELETHON_SESSIONS_FOLDER + data["phone_number"],
            data["api_id"],
            data["api_hash"],
        )
        try:
            await client.connect()
            await client.sign_in(
                data["phone_number"],
                data["verification_code"],
                phone_code_hash=data["phone_code_hash"],
            )
        except PhoneCodeInvalidError:
            await client.disconnect()
            await message.reply("Неверный код авторизации, попробуйте снова")
            await state.finish()
            return
        except FloodWaitError:
            await client.disconnect()
            await message.reply(
                "Слишком много запросов на авторизацию, попробуйте снова через некоторое время, либо используйте другой аккаунт"
            )
            await state.finish()
            return
        except:
            traceback.print_exc()
            await message.reply("Что то пошло не так, попробуйте снова")
            await state.finish()
            return

        is_authorized = await client.is_user_authorized()
        await client.disconnect()
        if is_authorized:
            token = get_jwt_token(message.from_user.id)
            request_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            data = {
                "api_id": data["api_id"],
                "api_hash": data["api_hash"],
                "phone_number": data["phone_number"],
                "is_initialized": True,
            }
            path = "telethon/accounts/"
            url = API_LINK_FOR_TELEGRAM_BOTS + path

            response = requests.post(url, headers=request_headers, json=data)

            if response.status_code == 201:
                await message.reply("Аккаунт успешно добавлен")
            elif response.status_code == 400:
                await message.reply("Что то пошло не так, выводим вам ошибку")
                await message.reply(response.text)
            else:
                await message.reply(
                    "Не удалось добавить аккаунт, внутренняя ошибка сервера"
                )
        else:
            await message.reply("что то пошло не так, попробуйте снова")
    # Finish conversation
    await state.finish()
