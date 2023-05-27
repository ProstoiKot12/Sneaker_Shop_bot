from aiogram import Bot, Dispatcher, executor, types
import config
import sql_request
import user_keyboards
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token=config.TOKEN)

name = ''

class UserState(StatesGroup):
    price_calculator = State()
    order_name = State()

async def start_handler(message: types.Message):
    await sql_request.cmd_start_db(message.from_user.id, message.from_user.username)
    if config.ADMIN_ID == message.from_user.id:
        await message.answer(f"Привет {message.from_user.first_name}, ты админ!\nЧтобы включить админ панель /panel\nЧтобы выключить /off", reply_markup=user_keyboards.main_panel)
    else:
        await message.answer(f"<b>Главное меню</b>", reply_markup=user_keyboards.main_panel, parse_mode='HTML')

async def price_calc(message: types.Message, state: FSMContext):
    product = message.text.strip()
    await sql_request.uan_calculator(float(product), message.from_user.id)
    await state.finish()

async def order_user_name(message: types.Message, state: FSMContext):
    await sql_request.order_request(message.text, message.from_user.username)
    await message.answer("Отлично! Наш менеджер  в течение дня свяжеться с вами чтобы обсудить детели заказа")
    await bot.send_message(config.ADMIN_ID, "<b>Появился новый заказ!\n</b>"
                                     "Посмотреть вы его сможете в админ панеле", parse_mode='HTML')
    await state.finish()

async def message_replay(message: types.Message):
    await message.answer("Команда не распознана")
