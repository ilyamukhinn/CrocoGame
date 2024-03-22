import asyncio
import logging

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

def create_db() -> None:
    mongo_db_manager.DBManager().create_films_collection()
    mongo_db_manager.DBManager().create_books_collection()
    mongo_db_manager.DBManager().create_statements_collection()
    mongo_db_manager.DBManager().create_characters_collection()

    mongo_db_manager.DBManager().create_categories_collection()


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
    create_db()
    asyncio.run(main())
