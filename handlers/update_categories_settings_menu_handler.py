from typing import Dict, Any
import sqlite3

import categories
import card

from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram import types

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Checkbox, Row, Cancel

from db import main_db_interface, user_db_tables

router = Router()


class UpdateCardSettings(StatesGroup):
    START = State()


SAVE_CARD_SETTINGS_BTN_ID = "save"
FILMS_CARD_SETTINGS_CHECK_BTN_ID = "films_check_btn"
PEOPLE_CARD_SETTINGS_CHECK_BTN_ID = "people_check_btn"
BOOKS_CARD_SETTINGS_CHECK_BTN_ID = "books_check_btn"


async def on_dialog_start(start_data: Any, dialog_manager: DialogManager):
    conn = sqlite3.connect(user_db_tables.user_db_path)
    user_category_data = main_db_interface.DBInterface.select_records(
        conn,
        user_db_tables.UserCategoryTable.user_category_user_id_field_name,
        dialog_manager.event.from_user.id,
        user_db_tables.UserCategoryTable.table_name,
    )

    for row in user_category_data:
        category = user_db_tables.CategoryTable.base_data_inverted.get(
            row[user_db_tables.UserCategoryTable.user_category_category_id_field_name],
            0,
        )
        if category:
            match category:
                case categories.Films:
                    dialog_manager.dialog_data["films_chosen"] = (
                        row[
                            user_db_tables.UserCategoryTable.user_category_category_chosen_field_name
                        ]
                        == 1
                    )
                    dialog_manager.dialog_data["films_no_chosen"] = (
                        not dialog_manager.dialog_data["films_chosen"]
                    )

                case categories.People:
                    dialog_manager.dialog_data["people_chosen"] = (
                        row[
                            user_db_tables.UserCategoryTable.user_category_category_chosen_field_name
                        ]
                        == 1
                    )
                    dialog_manager.dialog_data["people_no_chosen"] = (
                        not dialog_manager.dialog_data["people_chosen"]
                    )

                case categories.Books:
                    dialog_manager.dialog_data["books_chosen"] = (
                        row[
                            user_db_tables.UserCategoryTable.user_category_category_chosen_field_name
                        ]
                        == 1
                    )
                    dialog_manager.dialog_data["books_no_chosen"] = (
                        not dialog_manager.dialog_data["books_chosen"]
                    )


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "films_chosen": dialog_manager.dialog_data["films_chosen"],
        "films_no_chosen": dialog_manager.dialog_data["films_no_chosen"],
        "people_chosen": dialog_manager.dialog_data["people_chosen"],
        "people_no_chosen": dialog_manager.dialog_data["people_no_chosen"],
        "books_chosen": dialog_manager.dialog_data["books_chosen"],
        "books_no_chosen": dialog_manager.dialog_data["books_no_chosen"],
    }


async def save_card_settings(
    callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager
):
    conn = sqlite3.connect(user_db_tables.user_db_path)

    # ПОКА ЧТО БЕРЕМ МАКСИМАЛЬНОЕ ЧИСЛО СЛОВ ИЗ БАЗОВОГО ЗНАЧЕНИЯ
    categories_chosen_amount: int = 0
    categories_chosen_amount += (
        1 if dialog_manager.find(FILMS_CARD_SETTINGS_CHECK_BTN_ID).is_checked() else 0
    )
    categories_chosen_amount += (
        1 if dialog_manager.find(PEOPLE_CARD_SETTINGS_CHECK_BTN_ID).is_checked() else 0
    )
    categories_chosen_amount += (
        1 if dialog_manager.find(BOOKS_CARD_SETTINGS_CHECK_BTN_ID).is_checked() else 0
    )

    main_db_interface.DBInterface.update_record_and_operator(
        conn,
        user_db_tables.UserCategoryTable.user_category_user_id_field_name,
        callback.from_user.id,
        user_db_tables.UserCategoryTable.user_category_category_id_field_name,
        user_db_tables.CategoryTable.base_data[categories.Films],
        [
            user_db_tables.UserCategoryTable.user_category_category_chosen_field_name,
            user_db_tables.UserCategoryTable.user_category_category_words_in_card_field_name,
        ],
        [
            (
                1
                if dialog_manager.find(FILMS_CARD_SETTINGS_CHECK_BTN_ID).is_checked()
                else 0
            ),
            (
                0
                if not dialog_manager.find(
                    FILMS_CARD_SETTINGS_CHECK_BTN_ID
                ).is_checked()
                else card.Card.BASE_CARD_SETTINGS[card.Card.words_in_card_field_name]
                // categories_chosen_amount
            ),
        ],
        user_db_tables.UserCategoryTable.table_name,
    )

    main_db_interface.DBInterface.update_record_and_operator(
        conn,
        user_db_tables.UserCategoryTable.user_category_user_id_field_name,
        callback.from_user.id,
        user_db_tables.UserCategoryTable.user_category_category_id_field_name,
        user_db_tables.CategoryTable.base_data[categories.People],
        [
            user_db_tables.UserCategoryTable.user_category_category_chosen_field_name,
            user_db_tables.UserCategoryTable.user_category_category_words_in_card_field_name,
        ],
        [
            (
                1
                if dialog_manager.find(PEOPLE_CARD_SETTINGS_CHECK_BTN_ID).is_checked()
                else 0
            ),
            (
                0
                if not dialog_manager.find(
                    PEOPLE_CARD_SETTINGS_CHECK_BTN_ID
                ).is_checked()
                else card.Card.BASE_CARD_SETTINGS[card.Card.words_in_card_field_name]
                // categories_chosen_amount
            ),
        ],
        user_db_tables.UserCategoryTable.table_name,
    )

    main_db_interface.DBInterface.update_record_and_operator(
        conn,
        user_db_tables.UserCategoryTable.user_category_user_id_field_name,
        callback.from_user.id,
        user_db_tables.UserCategoryTable.user_category_category_id_field_name,
        user_db_tables.CategoryTable.base_data[categories.Books],
        [
            user_db_tables.UserCategoryTable.user_category_category_chosen_field_name,
            user_db_tables.UserCategoryTable.user_category_category_words_in_card_field_name,
        ],
        [
            (
                1
                if dialog_manager.find(BOOKS_CARD_SETTINGS_CHECK_BTN_ID).is_checked()
                else 0
            ),
            (
                0
                if not dialog_manager.find(
                    BOOKS_CARD_SETTINGS_CHECK_BTN_ID
                ).is_checked()
                else card.Card.BASE_CARD_SETTINGS[card.Card.words_in_card_field_name]
                // categories_chosen_amount
            ),
        ],
        user_db_tables.UserCategoryTable.table_name,
    )


card_settings = Dialog(
    Window(
        Const("Настройки карточки"),
        Checkbox(
            checked_text=Const("[✓] Фильмы {}".format(categories.Films.ICON)),
            unchecked_text=Const("[] Фильмы {}".format(categories.Films.ICON)),
            id=FILMS_CARD_SETTINGS_CHECK_BTN_ID,
            default=True,
            when="films_chosen",
        ),
        Checkbox(
            checked_text=Const("[✓] Фильмы {}".format(categories.Films.ICON)),
            unchecked_text=Const("[] Фильмы {}".format(categories.Films.ICON)),
            id=FILMS_CARD_SETTINGS_CHECK_BTN_ID,
            default=False,
            when="films_no_chosen",
        ),
        Checkbox(
            checked_text=Const("[✓] Личности {}".format(categories.People.ICON)),
            unchecked_text=Const("[] Личности {}".format(categories.People.ICON)),
            id=PEOPLE_CARD_SETTINGS_CHECK_BTN_ID,
            default=True,
            when="people_chosen",
        ),
        Checkbox(
            checked_text=Const("[✓] Личности {}".format(categories.People.ICON)),
            unchecked_text=Const("[] Личности {}".format(categories.People.ICON)),
            id=PEOPLE_CARD_SETTINGS_CHECK_BTN_ID,
            default=False,
            when="people_no_chosen",
        ),
        Checkbox(
            checked_text=Const("[✓] Книги {}".format(categories.Books.ICON)),
            unchecked_text=Const("[] Книги {}".format(categories.Books.ICON)),
            id=BOOKS_CARD_SETTINGS_CHECK_BTN_ID,
            default=True,
            when="books_chosen",
        ),
        Checkbox(
            checked_text=Const("[✓] Книги {}".format(categories.Books.ICON)),
            unchecked_text=Const("[] Книги {}".format(categories.Books.ICON)),
            id=BOOKS_CARD_SETTINGS_CHECK_BTN_ID,
            default=False,
            when="books_no_chosen",
        ),
        Row(
            Cancel(),
            Cancel(
                text=Const("Save"),
                id=SAVE_CARD_SETTINGS_BTN_ID,
                on_click=save_card_settings,
            ),
        ),
        state=UpdateCardSettings.START,
    ),
    on_start=on_dialog_start,
    getter=getter,
)

router.include_router(card_settings)
