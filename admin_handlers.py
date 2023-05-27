from aiogram import Bot, Dispatcher, executor, types
from config import CHAT_ID, ADMIN_ID, TOKEN
import user_keyboards
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from sql_request import *
import admin_keyboards
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)

class UserState(StatesGroup):
    admin_panel = State()
    forward_group1 = State()
    spam = State()
    course = State()
    order_delete = State()

async def admin_panel_on(message: types.Message):
    if ADMIN_ID == message.from_user.id:
        await message.answer('Админ панель включена', reply_markup=admin_keyboards.admin_panel)
        await UserState.admin_panel.set()
    else:
        await message.answer("Команда не распознана")

async def admin_panel(message: types.Message, state: FSMContext):
    if message.text == "📨 Рассылка в бота":
        await message.answer("Введите текст рассылки")
        await UserState.spam.set()
    elif message.text == "✉️ Сообщение в группу":
        await message.answer("Введите текст сообщения")
        await UserState.forward_group1.set()
    elif message.text == "¥ Изменить курс юаня":
        await message.answer("Введите курс юаня с точкой\n"
                             "Например 12.7")
        await UserState.course.set()
    elif message.text == "¥ Посмотреть курс юаня":
        await uan_look(message.from_user.id)
    elif message.text == "📜 Посмотреть заявки":
        await checking_order(message.from_user.id)
    elif message.text == "❌ Удалить заявку":
        await message.answer("Введите <b>user_name</b> пользователя чью заявку вы хотите удалить, без @\n"
                             "Например Yarosalvxxxxxx", parse_mode='HTML')
        await UserState.order_delete.set()
    elif message.text == "🟥 Выключить админ панель" or message.text == "/off":
        await message.answer('Админ панель выключена', reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer("Нажмите кнопку или выключите админ-панель")
        await UserState.admin_panel.set()

async def order_delete(message: types.Message, state: FSMContext):
    await delete_order(message.text.strip(), message.from_user.id)

async def uan_course(message: types.Message, state: FSMContext):
    price = message.text
    await create_uan(price)
    await message.answer(f'Курс юаня успешно обновлен на {price}')
    await UserState.admin_panel.set()

async def forward_group(message: types.Message, state: FSMContext):
    await bot.send_message(CHAT_ID, message.text)
    await message.answer("Сообщение отправлено в группу")
    await UserState.admin_panel.set()

async def spam_user(message: types.Message, state: FSMContext):
    await user_id(message)
    await message.answer("Сообщение отправлено пользователям")
    await UserState.admin_panel.set()

async def on_start():
    await bot.send_message(1002464520, "Бот запущен")

async def off_start():
    await bot.send_message(1002464520, "Бот остановлен")