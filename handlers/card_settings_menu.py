import asyncio
from typing import Dict, Any
import sqlite3

import categories
from handlers.categories_settings import (
    books_settings,
    films_settings,
    people_settings,
    statements_settings
    )
from handlers.categories_settings.category_settings import CategorySettingsCreator, CategorySettings

from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram import types

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Cancel, ScrollingGroup

from db import main_db_interface, user_db_tables

router = Router()


class UpdateCardSettings(StatesGroup):
    START = State()

WORDS_AMOUNT_BTN_ID = "words_amount_btn"
SETTING_GROUP_ID = "setting_group"
SAVE_CARD_SETTINGS_BTN_ID = "save"

async def on_dialog_start(start_data: Any, dialog_manager: DialogManager):
    conn = sqlite3.connect(user_db_tables.user_db_path)

    for category in categories.categories_types:
        query: str = """SELECT count({0}) FROM {1} WHERE {0} = ? AND {2} = ?""".format(
            user_db_tables.UserCategoryTable.user_category_user_id_field_name, 
            user_db_tables.UserCategoryTable.table_name, 
            user_db_tables.UserCategoryTable.user_category_category_id_field_name,
        )
        if not main_db_interface.DBInterface._record_exists(
            conn, 
            query, 
            (dialog_manager.event.from_user.id, user_db_tables.CategoryTable.base_data[category], )):
            main_db_interface.DBInterface.create_record(
                conn,
                user_db_tables.UserCategoryTable.fields_names_list,
                [
                    dialog_manager.event.from_user.id, 
                    user_db_tables.CategoryTable.base_data[category],
                    0,
                    0
                ],
                user_db_tables.UserCategoryTable.table_name)

    user_category_data = main_db_interface.DBInterface.select_records(
        conn,
        user_db_tables.UserCategoryTable.user_category_user_id_field_name,
        dialog_manager.event.from_user.id,
        user_db_tables.UserCategoryTable.table_name,
    )

    dialog_manager.dialog_data[CategorySettingsCreator.words_amount_key] = 0

    def get_user_category_info(
        row: dict[str, Any],
        chosen_key: str,
        no_chosen_key: str,
        amount_key: str
    ):
        dialog_manager.dialog_data[chosen_key] = \
            row[user_db_tables.UserCategoryTable.user_category_category_chosen_field_name] == 1
        dialog_manager.dialog_data[no_chosen_key] = \
            not dialog_manager.dialog_data[chosen_key]
        dialog_manager.dialog_data[amount_key] = \
            row[user_db_tables.UserCategoryTable.user_category_category_words_in_card_field_name]
        if dialog_manager.dialog_data[chosen_key]:
            dialog_manager.dialog_data[CategorySettingsCreator.words_amount_key] += \
                dialog_manager.dialog_data[amount_key]

    for row in user_category_data:
        category = user_db_tables.CategoryTable.base_data_inverted.get(
            row[user_db_tables.UserCategoryTable.user_category_category_id_field_name], 0)
        if category:
            match category:
                case categories.Films:
                    get_user_category_info(
                        row, 
                        films_settings.FilmsSettingsCreator().get_chosen_key(), 
                        films_settings.FilmsSettingsCreator().get_no_chosen_key(), 
                        films_settings.FilmsSettingsCreator().get_amount_key())
                case categories.People:
                    get_user_category_info(
                        row, 
                        people_settings.PeopleSettingsCreator().get_chosen_key(),
                        people_settings.PeopleSettingsCreator().get_no_chosen_key(),
                        people_settings.PeopleSettingsCreator().get_amount_key())
                case categories.Books:
                    get_user_category_info(
                        row, 
                        books_settings.BooksSettingsCreator().get_chosen_key(), 
                        books_settings.BooksSettingsCreator().get_no_chosen_key(),
                        books_settings.BooksSettingsCreator().get_amount_key())
                case categories.Statements:
                    get_user_category_info(
                        row,
                        statements_settings.StatementsSettingsCreator().get_chosen_key(),
                        statements_settings.StatementsSettingsCreator().get_no_chosen_key(),
                        statements_settings.StatementsSettingsCreator().get_amount_key())
                    

async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    dialog_data = {}
    categories: list[CategorySettingsCreator] = [
        films_settings.FilmsSettingsCreator(),
        people_settings.PeopleSettingsCreator(),
        books_settings.BooksSettingsCreator(),
        statements_settings.StatementsSettingsCreator()
        ]
    for category in categories:
        dialog_data.update(category.getter(dialog_manager))
    dialog_data.update({
        CategorySettingsCreator.words_amount_key: 
        dialog_manager.dialog_data[CategorySettingsCreator.words_amount_key]
        })
    return dialog_data


async def save_card_settings(
    callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager
):
    conn = sqlite3.connect(user_db_tables.user_db_path)

    category_settings: list[CategorySettingsCreator] = [
        films_settings.FilmsSettingsCreator(),
        people_settings.PeopleSettingsCreator(),
        books_settings.BooksSettingsCreator(),
        statements_settings.StatementsSettingsCreator()
        ]

    categories_chosen_amount: int = 0
    for category in category_settings:
        categories_chosen_amount += int(category.get_if_category_chosen(dialog_manager))

    if categories_chosen_amount < 1:
        await callback.answer("Должна быть выбрана хотя бы одна категория!", show_alert=True)
        return
    
    words_chosen_amount: int = 0
    for category in category_settings:
        words_chosen_amount += int(category.get_category_amount_if_chosen(dialog_manager))


    if not words_chosen_amount == 6:
        await callback.answer("Общее количество слов по выбранным категориям должно быть равно 6!", show_alert=True)
        await callback.answer()
        return
    
    for category_type, category in zip(
        categories.categories_types, 
        category_settings):

        main_db_interface.DBInterface.update_record_and_operator(
            conn,
            user_db_tables.UserCategoryTable.user_category_user_id_field_name,
            callback.from_user.id,
            user_db_tables.UserCategoryTable.user_category_category_id_field_name,
            user_db_tables.CategoryTable.base_data[category_type],
            [
                user_db_tables.UserCategoryTable.user_category_category_chosen_field_name,
                user_db_tables.UserCategoryTable.user_category_category_words_in_card_field_name,
            ],
            [
                int(dialog_manager.find(category.get_card_settings_check_btn_id()).is_checked()),
                (
                    0
                    if not dialog_manager.find(
                        category.get_card_settings_check_btn_id()
                    ).is_checked()
                    else dialog_manager.dialog_data[category.get_amount_key()]
                ),
            ],
            user_db_tables.UserCategoryTable.table_name,
        )

    dump = await callback.message.answer("Настройки сохранены!")
    await dialog_manager.done()

    await asyncio.sleep(5)
    try:
        await dump.delete()
    except Exception as e:
        pass

async def show_card_settings(
    callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager
):
    categories: list[CategorySettingsCreator] = [
        films_settings.FilmsSettingsCreator(),
        people_settings.PeopleSettingsCreator(),
        books_settings.BooksSettingsCreator(),
        statements_settings.StatementsSettingsCreator()
        ]
    message: str = "Текущие настройки"
    for category in categories:
        message += "\n" + category.get_current_category_settings(dialog_manager)

    await callback.answer(message, show_alert=True)

def CreateScrollingGroup() -> list[Any]:
    categories: list[CategorySettingsCreator] = [
        films_settings.FilmsSettingsCreator(),
        people_settings.PeopleSettingsCreator(),
        books_settings.BooksSettingsCreator(),
        statements_settings.StatementsSettingsCreator()
        ]
    buttons = []
    for category in categories:
        buttons += category.category_group_creator()

    return buttons

card_settings = Dialog(
    Window(
        Const("Настройки карточки"),
        ScrollingGroup(*CreateScrollingGroup(), 
            id=SETTING_GROUP_ID, width=2, height=2),
        Button(text=Format("Выбрано всего слов: {dialog_data[words_amount]}"), id=WORDS_AMOUNT_BTN_ID, on_click=show_card_settings),
        Row(
            Cancel(text=Const("Назад")),
            Button(text=Const("Сохранить"), id=SAVE_CARD_SETTINGS_BTN_ID, on_click=save_card_settings),
        ),
        state=UpdateCardSettings.START,
    ),
    on_start=on_dialog_start,
    getter=getter,
)

router.include_router(card_settings)
