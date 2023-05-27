from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import admin_handlers
from user_handlers import *
from sql_request import *
from user_callback import *
import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

dp.register_message_handler(start_handler, commands=['start'])
dp.register_message_handler(admin_handlers.admin_panel_on, commands=['panel'])

dp.register_callback_query_handler(user_question, text=('question'))
dp.register_callback_query_handler(user, text=('popular_question'))
dp.register_callback_query_handler(calculator, text=('calculator'))
dp.register_callback_query_handler(delivery, text=('delivery'))
dp.register_callback_query_handler(opt, text=('opt'))
dp.register_callback_query_handler(main_menu, text=('main_menu'))
dp.register_callback_query_handler(order_start, text=('order'))

dp.register_message_handler(price_calc, state=UserState.price_calculator)
dp.register_message_handler(admin_handlers.order_delete, state=admin_handlers.UserState.order_delete)
dp.register_message_handler(admin_handlers.admin_panel, state=admin_handlers.UserState.admin_panel)
dp.register_message_handler(admin_handlers.uan_course, state=admin_handlers.UserState.course)
dp.register_message_handler(admin_handlers.forward_group, state=admin_handlers.UserState.forward_group1)
dp.register_message_handler(admin_handlers.spam_user, state=admin_handlers.UserState.spam)
dp.register_message_handler(order_user_name, state=UserState.order_name)
dp.register_message_handler(message_replay, content_types=types.ContentType.ANY)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)