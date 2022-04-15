from apps.telegram_bot.management.loaders.telegram_manual_bot_loader import dp
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types


class Form(StatesGroup):
    target_grooup = State()  # group to which subscribers will be added
    donor_group = State()  # subscriber donor group

@dp.message_handler(Command("invite"))
@dp.message_handler(text="Приглашения")
async def promotion_invitations(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await message.reply("Укажите ссылку на группу в которую будем инвайтить подписчиков !")
    await Form.target_grooup.set()

@dp.message_handler(state=Form.target_grooup)
async def save_target_grooup(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
      data["target_grooup"] = answer

    await message.answer("Укажите ссылку на группу донор подписчиков")
    await Form.donor_group.set()

@dp.message_handler(state=Form.donor_group)
async def save_donor_froup(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
      data["donor_froup"] = answer

    target_grooup = await state.get("target_grooup")
    donor_group = await state.get("donor_froup")

    await message.answer("Проверьте правильность указанных данных:")
    await message.answer(f"Целевая группа: {target_grooup}")
    await message.answer(f"Группа донор: {donor_group}")
    