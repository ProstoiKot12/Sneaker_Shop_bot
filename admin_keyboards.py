from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery

spam = KeyboardButton("📨 Рассылка в бота")
forward_group = KeyboardButton("✉️ Сообщение в группу")
checking = KeyboardButton("📜 Посмотреть заявки")
check_delete = KeyboardButton("❌ Удалить заявку")
course = KeyboardButton("¥ Изменить курс юаня")
course_look = KeyboardButton("¥ Посмотреть курс юаня")
off = KeyboardButton("🟥 Выключить админ панель")
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True).add(spam, forward_group).row(course, course_look).row(checking, check_delete).row(off)
