from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_start_menu_keyboard_builder() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="Получить карточку"))
    builder.row(
        types.KeyboardButton(text="Настройки"),
        types.KeyboardButton(text="Правила игры"),
    )
    builder.row(
        types.KeyboardButton(text="Помощь"),
        types.KeyboardButton(text="Поддержите разработчиков"),
    )

    return builder
