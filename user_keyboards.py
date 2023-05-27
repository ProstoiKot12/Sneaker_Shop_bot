from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery

menu = InlineKeyboardButton("◀️Вернуться в главное меню", callback_data='main_menu')
menu_kb = InlineKeyboardMarkup().add(menu)

cost_calculator = InlineKeyboardButton("💰Калькулятор стоимости", callback_data='calculator')
quastion = InlineKeyboardButton("👨‍💻По вопросам", callback_data='question')
place_order = InlineKeyboardButton("🛍️Оформить заказ", callback_data='order')
main_panel = InlineKeyboardMarkup(row_width=1).add(cost_calculator, quastion, place_order)

price_calculator = InlineKeyboardButton("🔁Расчитать ещё раз", callback_data='calculator')
price_calculator_kb = InlineKeyboardMarkup(row_width=1).add(price_calculator, menu)

popular_question = InlineKeyboardButton("❓Самые популярные вопросы", callback_data='popular_question')
most_question = InlineKeyboardMarkup(row_width=1).add(popular_question, menu)

delivery_question = InlineKeyboardButton("Сколько времени занимает доставка товара?", callback_data='delivery')
opt_question = InlineKeyboardButton("Будет ли цена дешевле, если заказать несколько вещей?", callback_data='opt')
delivery_kb = InlineKeyboardMarkup(row_width=1).add(delivery_question, opt_question, menu)


