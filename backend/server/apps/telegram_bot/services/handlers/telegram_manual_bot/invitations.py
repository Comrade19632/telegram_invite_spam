from json import loads

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from apps.telegram_bot.constants import API_LINK_FOR_TELEGRAM_BOTS
from apps.telegram_bot.management.loaders.telegram_manual_bot_loader import dp
from apps.telegram_bot.services import get_jwt_token


class Form(StatesGroup):
    target_chat_link = State()  # group to which subscribers will be added
    donor_chat_link = State()  # subscriber donor group
    create_order = State()


@dp.message_handler(Command("invite"))
@dp.message_handler(text="Приглашения")
async def promotion_invitations(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await message.reply(
        "Укажите ссылку на группу в которую будем инвайтить подписчиков !"
    )
    await Form.target_chat_link.set()


@dp.message_handler(state=Form.target_chat_link)
async def save_target_chat_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["target_chat_link"] = message.text

    await message.answer("Укажите ссылку на группу донор подписчиков")
    await Form.donor_chat_link.set()


@dp.message_handler(state=Form.donor_chat_link)
async def save_donor_chat_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["donor_chat_link"] = message.text
        await message.answer("Проверьте правильность указанных данных:")
        await message.answer(f"Целевая группа: {data['target_chat_link']}")
        await message.answer(f"Группа донор: {data['donor_chat_link']}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Да", "Нет")
    await message.reply("Все верно?", reply_markup=markup)
    await Form.create_order.set()


@dp.message_handler(state=Form.create_order)
async def create_order(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    if message.text == "Нет":
        await message.reply("Программа отменена", reply_markup=markup)
        await state.finish()
        return
    async with state.proxy() as data:
        token = get_jwt_token(message.from_user.id)
        request_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {
            "target_chat_link": data["target_chat_link"],
            "donor_chat_link": data["donor_chat_link"],
        }
        path = "orders/invite/"
        url = API_LINK_FOR_TELEGRAM_BOTS + path

        response = requests.post(url, headers=request_headers, json=data)

        if response.status_code == 201:
            await message.reply("Заказ на инвайт успешно добавлен", reply_markup=markup)
        elif response.status_code == 400:
            await message.reply(
                "Что то пошло не так, выводим вам ошибку", reply_markup=markup
            )
            await message.reply(response.text)
            await state.finish()
            return
        else:
            await message.reply(
                "Не удалось добавить заказ на инвайт, внутренняя ошибка сервера",
                reply_markup=markup,
            )
            await state.finish()
            return

        order = loads(response.text)
        request_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        path = f"orders/invite/{order['id']}/start/"
        url = API_LINK_FOR_TELEGRAM_BOTS + path

        response = requests.get(url, headers=request_headers)

        if response.status_code == 200:
            await message.reply("Запрос на активацию инвайта успешно отправлен")
            await state.finish()
            return
        elif response.status_code == 404:
            await message.reply("Что то пошло не так, выводим вам ошибку")
            await message.reply(response.text)
            await state.finish()

            return
        else:
            await message.reply(
                "Не удалось добавить заказ на инвайт, внутренняя ошибка сервера"
            )
            await state.finish()
            return