import asyncio
import logging
import sqlite3
import os

import categories
from db import main_db_interface, user_db_tables
from db.mongo import mongo_db_manager

from handlers import (
    main_menu_keyboard,
    maintenance_handler,
    update_chat_membership,
)
from config_reader import config

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.message import ContentType
from aiogram_dialog import setup_dialogs

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp["films"] = categories.Films()
dp["people"] = categories.People()
dp["books"] = categories.Books()
dp["statements"] = categories.Statements()

def _create_db() -> None:
    mongo_db_manager.DBManager().create_films_collection()
    mongo_db_manager.DBManager().create_books_collection()
    mongo_db_manager.DBManager().create_statements_collection()
    mongo_db_manager.DBManager().create_characters_collection()

    mongo_db_manager.DBManager().create_categories_collection()
    mongo_db_manager.DBManager().get_films_sample(3)
    

def create_db() -> None:
    conn = sqlite3.connect(user_db_tables.user_db_path)

    for table_name, fields in user_db_tables.user_db_tables_full_info.items():
        if main_db_interface.DBInterface.table_exists(conn, table_name):
            print("Table exists")
        else:
            main_db_interface.DBInterface.create_talbe(conn, fields, table_name)

            if table_name == user_db_tables.CategoryTable.table_name:
                for category_name, id in user_db_tables.CategoryTable.base_data.items():
                    main_db_interface.DBInterface.create_record(
                        conn,
                        [
                            user_db_tables.CategoryTable.category_id_field_name,
                            user_db_tables.CategoryTable.category_name_field_name,
                        ],
                        [id, "'{}'".format(category_name.CATEGORY_NAME_ENG)],
                        user_db_tables.CategoryTable.table_name,
                    )


async def setup_bot_commands():
    bot_commands = [
        types.BotCommand(command="/start", description="Мы можем снова поприветствовать друг друга! 👋"),
        types.BotCommand(command="/help", description="Получи информация обо мне ℹ️"),
        types.BotCommand(command="/settings", description="Меню настроек игры ⚙️"),
        types.BotCommand(command="/rules", description="Получи информацию о правилах игры ⚖️"),
        types.BotCommand(command="/get_card", description="Сгенерируй новую карточку 🃏"),
        types.BotCommand(command="/donate", description="Помоги авторам собрать на пиццу 🍕"),
    ]
    await bot.set_my_commands(bot_commands)

PRICE = types.LabeledPrice(label="На пиццу", amount=100*100)  # в копейках (руб)

@dp.message(F.text.lower() == "поддержите разработчиков 💰")
@dp.message(Command("donate"))
async def cmd_donate(message: types.Message):
    if config.payments_token.get_secret_value().split(':')[1] == 'TEST':
        await bot.send_message(chat_id=message.chat.id, text="Тестовый платеж!")

    await bot.send_invoice(message.chat.id,
                           title="Поддержка разработчиков",
                           description="Спасибо, что неравнодушны к этому проекту!",
                           provider_token=config.payments_token.get_secret_value(),
                           currency="rub",
                           photo_url="https://sun1-93.userapi.com/s/v1/ig2/BwKnuY9jbroEehJfHb5SxSlV2TMXYtbXBuPnp2dtg1BayC9lnxacooevC3zQ2S_FpVvbPXzMGrE4nO0poI1X0IDK.jpg?size=898x898&quality=96&crop=1,0,898,898&ava=1",
                           photo_width=416,
                           photo_height=400,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="pizza-support",
                           payload="test-invoice-payload")

# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!")

async def main():
    dp.startup.register(setup_bot_commands)
    dp.include_routers(
        main_menu_keyboard.router,
        maintenance_handler.maintenance_router,
        update_chat_membership.router,
    )
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    _create_db()
    create_db()
    asyncio.run(main())
