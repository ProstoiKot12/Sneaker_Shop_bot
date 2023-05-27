from aiogram import Bot, Dispatcher, executor, types
import config
import user_keyboards
import sql_request
from user_handlers import *

bot = Bot(token=config.TOKEN)

async def main_menu(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(f"<b>Главное меню</b>", reply_markup=user_keyboards.main_panel, parse_mode='HTML')

async def user_question(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("❓<b>Задать вопросы вы можете нашему менеджеру</b>\n\n"
                                        "@YaroslavGavrilov1\n\n"
                                        "Ему вы можете задвать вопрос по любой теме которая вас интересует", reply_markup=user_keyboards.most_question, parse_mode='HTML')

async def delivery(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    await callback_query.message.answer("🚚 <b>Сколько времени занимает доставка товара?</b>\n\n"
                                        "Доставка со склада в Китае до склада в России (г. Казань) занимает около 25 дней, <b>НО</b>\n\n"
                                        "Стоит понимать, что после оплаты товара в боте товар попадает в базу данных. Из-за разницы во времени товар может выкупаться в течении 12-24 часов.\n\n"
                                        "После выкупа товара начинается доставка товара по Китаю на наш склад. Доставка по Китаю после выкупа может занимать от 1 до 14 дней (если мы говорим про площадку POIZON).\n"
                                        "Товары с Taobao, 1688 и других китайских площадок прибывают на склад как правило в течении 3-5 дней.\n\n"
                                        "Итого весь цикл доставки с площадки POIZON в худшем случае может занимать около 40 дней.\n"
                                        "Цикл доставки с других площадок занимает примерно 30 дней.\n\n"
                                        "Доставка по России в эти диапазоны <b>не входит</b> и зависит от удаленности Вашего региона от г. Казань.",
                                        parse_mode='HTML', reply_markup=user_keyboards.most_question,)

async def opt(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    await callback_query.message.answer("🛍 <b>Будет ли цена дешевле, если заказать несколько вещей?</b>\n\n"
                                        "<b>Краткий ответ: ✅Да и ❌Нет</b>\n\n"
                                        "✅<b>Когда да?</b>У нас действуют специальные условия для оптовиков и дропшипперов. Минимальный заказ от 10 любых позиций за раз.\n\n"
                                        "❌<b>Когда нет?</b> Если Вы хотите заказать 2-3 позиции, то к сожалению комиссия за предоставление услуг будет фиксированной.", parse_mode='HTML', reply_markup=user_keyboards.most_question)

async def user(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    await callback_query.message.answer('<b>Популярные вопросы</b>', reply_markup=user_keyboards.delivery_kb, parse_mode='HTML')

async def calculator(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Введите стоимость товара в юанях")
    await UserState.price_calculator.set()

async def order_start(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await sql_request.order_check(callback_query.from_user.username, callback_query.from_user.id)

