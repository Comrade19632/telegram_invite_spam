import datetime
from json import dumps, loads

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
    was_online_delta_users_settings = State()
    get_recently_online_users_users_settings = State()
    create_order = State()
    check_for_similar_orders = State()


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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("1 час назад", "1 день назад", "3 дня назад", "Всех пользователей")
    await message.reply(
        "Каких пользователей парсить из группы донора? (онлайн не больше чем)",
        reply_markup=markup,
    )
    await Form.was_online_delta_users_settings.set()


@dp.message_handler(state=Form.was_online_delta_users_settings)
async def save_was_online_delta_users_settings(
    message: types.Message, state: FSMContext
):
    async with state.proxy() as data:
        data["was_online_user_delta"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Да", "Нет")
    await message.reply(
        "Парсить пользователей которые были в сети недавно? (скрыт статус онлайна)",
        reply_markup=markup,
    )
    await Form.get_recently_online_users_users_settings.set()


@dp.message_handler(state=Form.get_recently_online_users_users_settings)
async def save_get_recently_online_users_users_settings(
    message: types.Message, state: FSMContext
):
    async with state.proxy() as data:
        data["get_recently_online_users"] = message.text
        await message.answer("Проверьте правильность указанных данных:")
        await message.answer(f"Целевая группа: {data['target_chat_link']}")
        await message.answer(f"Группа донор: {data['donor_chat_link']}")
        await message.answer(
            f"Каких пользователей парсим (онлайн не больше чем): {data['was_online_user_delta']}"
        )
        await message.answer(
            f"Парсим пользователей у которых скрыт онлайн: {data['get_recently_online_users']}"
        )
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
        post_data = {
            "target_chat_link": data["target_chat_link"],
            "donor_chat_link": data["donor_chat_link"],
            "was_online_user_delta": get_was_online_delta_from_text(
                data["was_online_user_delta"]
            ),
            "get_recently_online_users": True
            if data["get_recently_online_users"] == "Да"
            else False,
        }
        path = "orders/invite/"
        url = API_LINK_FOR_TELEGRAM_BOTS + path

        response = requests.post(
            url, headers=request_headers, data=dumps(post_data, default=str)
        )

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

        data["order_id"] = order["id"]

        request_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        path = f"orders/invite?target_chat_link={data['target_chat_link']}&donor_chat_link={data['donor_chat_link']}"
        url = API_LINK_FOR_TELEGRAM_BOTS + path

        response = requests.get(url, headers=request_headers)

        if not response.status_code == 200:
            await message.reply("Внутренняя ошибка сервера, попробуйте снова")
            await state.finish()
            return

        orders = loads(response.text)
        data["similar_orders_ids"] = []
        for order in orders:
            if not order["id"] == data["order_id"]:
                data["similar_orders_ids"].append(order["id"])

        if data["similar_orders_ids"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add("Да", "Нет")
            await message.reply(
                "Найдены ваши заказы с одинаковыми целевыми и группами донорами, скопировать из них уже приглашённых пользователей?",
                reply_markup=markup,
            )
            await Form.check_for_similar_orders.set()

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add("Активировать заказ")
            await message.reply(
                "Аквитируйте заказ",
                reply_markup=markup,
            )
            await Form.check_for_similar_orders.set()


@dp.message_handler(state=Form.check_for_similar_orders)
async def check_for_similar_orders(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        markup = types.ReplyKeyboardRemove()
        if message.text == "Да":
            token = get_jwt_token(message.from_user.id)
            request_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            post_data = {
                "similar_orders_ids": data["similar_orders_ids"],
            }
            path = f"orders/invite/{data['order_id']}/merge-with-similar-orders/"
            url = API_LINK_FOR_TELEGRAM_BOTS + path

            response = requests.post(url, headers=request_headers, json=post_data)

            if not response.status_code == 200:
                await message.reply(
                    "Внутренняя ошибка сервера, попробуйте снова", reply_markup=markup
                )
                await state.finish()
                return

            await message.reply(
                "Приглашенные пользователи успешно скопированы из других заказов",
                reply_markup=markup,
            )

        token = get_jwt_token(message.from_user.id)

        request_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        path = f"orders/invite/{data['order_id']}/start/"
        url = API_LINK_FOR_TELEGRAM_BOTS + path

        response = requests.get(url, headers=request_headers)

        if response.status_code == 200:
            await message.reply(
                "Запрос на активацию инвайта успешно отправлен", reply_markup=markup
            )
            await state.finish()
            return
        elif response.status_code == 404:
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


def get_was_online_delta_from_text(text):
    if text == "1 час назад":
        return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            hours=1
        )
    elif text == "1 день назад":
        return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    elif text == "3 дня назад":
        return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=3)
    else:
        return
