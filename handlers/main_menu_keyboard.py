import sqlite3

import card
import categories
from db import main_db_interface
from db import user_db_tables

from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji

from aiogram_dialog import DialogManager

from middlewares import long_operation_action_middlware
from keyboards import main_menu_reply_keyboard
from handlers import settings_menu
from db.mongo import mongo_db_manager

from models import (
    film_model, 
    book_model, 
    character_model, 
    statement_model)

from config_reader import config

router = Router()
router.include_routers(settings_menu.router)
router.callback_query.outer_middleware(
    long_operation_action_middlware.ChatActionMiddleware()
)

def _register_user(user_id: int) -> None:
    mongo_db_manager.DBManager().insert_user(user_id)

    for index, c in enumerate([
        film_model.Film.AdditionalData.CATEGORY_NAME_ENG,
        book_model.Book.AdditionalData.CATEGORY_NAME_ENG,
        statement_model.Statement.AdditionalData.CATEGORY_NAME_ENG,
        character_model.Character.AdditionalData.CATEGORY_NAME_ENG]):
        category = mongo_db_manager.DBManager().get_category(c)
        user = mongo_db_manager.DBManager().get_user(user_id)
        mongo_db_manager.DBManager().insert_user_category(user, category, 2 if index < 3 else 0)

def register_user(user_id: int) -> None:
    conn = sqlite3.connect(user_db_tables.user_db_path)
    if main_db_interface.DBInterface.record_exists(
        conn,
        user_db_tables.UserTable.user_id_field_name,
        user_id,
        user_db_tables.UserTable.table_name,
    ):
        print("User exists")
    else:
        main_db_interface.DBInterface.create_record(
            conn,
            user_db_tables.UserTable.fields_names_list,
            [
                user_id,
                card.Card.BASE_CARD_SETTINGS[card.Card.roll_dice_field_name],
                card.Card.BASE_CARD_SETTINGS[card.Card.words_in_card_field_name],
            ],
            user_db_tables.UserTable.table_name,
        )

        for count, (category, id) in enumerate(
            user_db_tables.CategoryTable.base_data.items()
        ):
            if count < 6:
                category_chosen: bool = card.Card.BASE_CARD_SETTINGS[
                    card.Card.categories_field_name
                ][category][card.Card.category_chosen_field_name]
                main_db_interface.DBInterface.create_record(
                    conn,
                    user_db_tables.UserCategoryTable.fields_names_list,
                    [
                        user_id,
                        id,
                        1 if category_chosen else 0,
                        (
                            card.Card.BASE_CARD_SETTINGS[
                                card.Card.categories_field_name
                            ][category][card.Card.category_words_in_card_field_name]
                            if category_chosen
                            else 0
                        ),
                    ],
                    user_db_tables.UserCategoryTable.table_name,
                )


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    _register_user(message.from_user.id)
    register_user(message.from_user.id)
    await message.answer(
        text="Привет! Меня зовут Филипп, и я могу помочь тебе "
        "отдохнуть от рабочих будней, ты можешь сыграть со "
        'мной в игру "Крокодил"🐊\n'
        "Чтобы узнать подробней о моих возможностях, перейди "
        "в меню и выбери команду /help или нажми на неё прямо "
        "здесь!",
        reply_markup=main_menu_reply_keyboard.make_start_menu_keyboard_builder().as_markup(
            resize_keyboard=True
        ),
    )


@router.message(
    F.text.lower() == "получить карточку 🃏", flags={"long_operation": "typing"}
)
@router.message(Command("get_card"), flags={"long_operation": "typing"})
async def cmd_get_game_card(
    message: types.Message,
    films: categories.Films,
    people: categories.People,
    books: categories.Books,
    statements: categories.Statements
):
    card_data: dict[str, any] = card.Card.generate_card(
        message.from_user.id,
        {
            films.CATEGORY_NAME_ENG: films,
            people.CATEGORY_NAME_ENG: people,
            books.CATEGORY_NAME_ENG: books,
            statements.CATEGORY_NAME_ENG: statements,
        },
    )
    await message.answer(text=card_data[card.Card.card_text_field_name])
    if card_data[user_db_tables.UserTable.dice_field_name]:
        await message.answer_dice(emoji=DiceEmoji.DICE)


@router.message(F.text.lower() == "настройки ⚙️")
@router.message(Command("settings"))
async def cmd_settings(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(settings_menu.Settings.START)

@router.message(F.text.lower() == "бросить кубик 🎲")
async def cmd_settings(message: types.Message, dialog_manager: DialogManager):
    await message.answer_dice(emoji=DiceEmoji.DICE)

@router.message(F.text.lower() == "помощь ℹ️")
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(text="Здесь будет справка о приложении")


@router.message(F.text.lower() == "правила игры ⚖️")
@router.message(Command("rules"))
async def cmd_rules(message: types.Message):
    await message.answer(text="Здесь будет справка о правилах игры")


@router.message(F.text)
async def cmd_missing(message: types.Message):
    await message.answer(text="Не знаю такой команды :(")
