import sqlite3
from datetime import date

import admin_handlers
import user_keyboards
from config import *
from aiogram import Bot, Dispatcher
import user_callback

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

con = sqlite3.connect("User.db")
cur = con.cursor()

async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS user_table("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id INTEGER, "
                "user_name TEXT)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS info_table("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "uan_course REAL DEFAULT 1, "
                "info TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS order_table("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT, "
                "user_name TEXT, "
                "date TEXT)")
    con.commit()

async def order_check(user_name, user_id):
    us_name = cur.execute("SELECT * FROM order_table WHERE user_name = ?", (user_name,)).fetchone()
    if not us_name:
        await bot.send_message(user_id,"👶<b>Пожалуйста, введите ФИО полностью как в паспорте (например Иванов Иван Иванович):</b>\n\n"
                                        "*на эти данные будет отправлена Ваша посылка", parse_mode='HTML')
        await user_callback.UserState.order_name.set()
    else:
        await bot.send_message(user_id, "Вы уже подали заявку\n"
                                        "Дождитесь пока менеджер вам напишет")

async def order_request(name, user_name):
    order = cur.execute("SELECT * FROM order_table WHERE user_name = ?", (user_name,)).fetchone()
    if not order:
        today = date.today()
        cur.execute("INSERT INTO order_table (name, user_name, date) VALUES (?, ?, ?)", (name, user_name, today))
        con.commit()

async def cmd_start_db(user_id, user_name):
    user1 = cur.execute("SELECT * FROM user_table WHERE user_id == {key}".format(key=user_id)).fetchone()
    if not user1:
        cur.execute("INSERT INTO user_table (user_id, user_name) VALUES (?, ?)", (user_id, f"@{user_name}"))
        con.commit()

async def user_id(message):
    cur.execute("SELECT user_id FROM user_table")
    us_id = cur.fetchall()
    for z in range(len(us_id)):
        await bot.send_message(us_id[z][0], message.text)

async def create_uan(price):
    cur.execute("SELECT uan_course FROM info_table")
    uan = cur.fetchall()
    if not uan:
        cur.execute("INSERT INTO info_table (uan_course) VALUES (?)", (price, ))
        con.commit()
    cur.execute("UPDATE info_table SET uan_course=?", (price, ))
    con.commit()

async def uan_calculator(product, user_id):
    cur.execute("SELECT uan_course FROM info_table WHERE id=1")
    uan = cur.fetchall()[0][0]

    price = int(round(product * uan, 1))
    price1 = int(round(price * 1.22, 1))

    await bot.send_message(user_id, f"Стоимость вашего товара состовляет <b>{price1}</b> рублей\n\n"
                                    f"<b>Уже включено:\n"
                                    "🚘Доставка до склада в России;\n"
                                    "💸Страховка 100% (если товар был украден или потерян Вам вернут 100% уплаченых средств).</b>\n\n"
                                    "Стоимость доставки товара по России оплачивается отдельно согласно тарифам транспортных компаний.\n\n"
                                    "<b>Сколько стоит доставка по России?</b> Рассчитать доставку Вы можете на сайте выбранной транспортной компании.", parse_mode='HTML', reply_markup=user_keyboards.price_calculator_kb)

async def uan_look(user_id):
    cur.execute("SELECT uan_course FROM info_table WHERE id=1")
    uan = cur.fetchall()[0][0]
    await bot.send_message(user_id, f"Курс юаня заданый в бота на данны момент состовляет <b>{uan}</b>", parse_mode='HTML')

async def checking_order(user_id):
    cur.execute("SELECT * FROM order_table")

    orders = cur.fetchall()
    info = ''
    for el in orders:
        info += f"\n\nФИО: {el[1]}\n\nUser_name: @{el[2]}\n\nДата: {el[3]}"

    await bot.send_message(user_id, f"<b>Вот все заявки</b> {info}", parse_mode="HTML")

async def delete_order(user_name, user_id):
    sql_delete = "DELETE from order_table WHERE user_name = ?"
    cur.execute(sql_delete, (user_name,))
    con.commit()
    await bot.send_message(user_id, "Удаление заявки завершено")
    await admin_handlers.UserState.admin_panel.set()

async def on_startup(_):
    await db_start()

