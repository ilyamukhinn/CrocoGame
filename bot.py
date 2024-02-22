import asyncio
import logging
import sqlite3

import categories
from db import main_db_interface, user_db_tables

from handlers import (
    main_menu_keyboard_handler,
    maintenance_handler,
    update_chat_membership,
)
from config_reader import config

from aiogram import Bot, Dispatcher, types, F

from aiogram_dialog import setup_dialogs

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp["films"] = categories.Films()
dp["people"] = categories.People()
dp["books"] = categories.Books()


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
        types.BotCommand(command="/start", description="We can greet each other!"),
        types.BotCommand(command="/help", description="Get info about me"),
        types.BotCommand(command="/settings", description="Game settings menu"),
        types.BotCommand(command="/rules", description="View game rules"),
        types.BotCommand(command="/get_card", description="Generate game card"),
        types.BotCommand(
            command="/donate", description="Donate to the authors for pizza"
        ),
    ]
    await bot.set_my_commands(bot_commands)


async def main():
    dp.startup.register(setup_bot_commands)
    dp.include_routers(
        main_menu_keyboard_handler.router,
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
    create_db()
    asyncio.run(main())
