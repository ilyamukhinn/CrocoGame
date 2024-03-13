import asyncio
from typing import Dict, Any
from db.mongo import mongo_db_manager

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

router = Router()

class UpdateCardSettings(StatesGroup):
    START = State()

WORDS_AMOUNT_BTN_ID = "words_amount_btn"
SETTING_GROUP_ID = "setting_group"
SAVE_CARD_SETTINGS_BTN_ID = "save"

async def on_dialog_start(start_data: Any, dialog_manager: DialogManager):
    categories_types = mongo_db_manager.DBManager().get_all_categories()
    user = mongo_db_manager.DBManager().get_user(dialog_manager.event.from_user.id)

    for category_type in categories_types:
        if mongo_db_manager.DBManager().get_user_category(user, category_type) is None:
            mongo_db_manager.DBManager().insert_user_category(user, category_type, 0)
        
    user_categories = mongo_db_manager.DBManager().get_user_categories(user.user_id)

    def get_user_category_info(
        amount: int,
        chosen_key: str,
        no_chosen_key: str,
        amount_key: str
    ):
        dialog_manager.dialog_data[chosen_key] = amount != 0
        dialog_manager.dialog_data[no_chosen_key] = amount == 0
        dialog_manager.dialog_data[amount_key] = amount if amount else 0
        dialog_manager.dialog_data[CategorySettingsCreator.words_amount_key] = \
            dialog_manager.dialog_data.get(CategorySettingsCreator.words_amount_key, 0) + amount if amount else \
                dialog_manager.dialog_data.get(CategorySettingsCreator.words_amount_key, 0) + 0

    categories: list[CategorySettingsCreator] = [
        films_settings.FilmsSettingsCreator(),
        people_settings.PeopleSettingsCreator(),
        books_settings.BooksSettingsCreator(),
        statements_settings.StatementsSettingsCreator()
        ]

    for row in user_categories:
        for category in categories:
            if row.category.name == category.get_category_name_eng():
                get_user_category_info(
                    row.amount, 
                    category.get_chosen_key(), 
                    category.get_no_chosen_key(), 
                    category.get_amount_key())
                    

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
    category_settings: list[CategorySettingsCreator] = [
        films_settings.FilmsSettingsCreator(),
        people_settings.PeopleSettingsCreator(),
        books_settings.BooksSettingsCreator(),
        statements_settings.StatementsSettingsCreator()
        ]
    
    categories_types = mongo_db_manager.DBManager().get_all_categories()

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
    
    user = mongo_db_manager.DBManager().get_user(callback.from_user.id)
    for category_type in categories_types:
        for category_setting in category_settings:
            if category_type.name == category_setting.get_category_name_eng():
                amount: int = 0
                if dialog_manager.find(category_setting.get_card_settings_check_btn_id()).is_checked():
                    amount = dialog_manager.dialog_data[category_setting.get_amount_key()]
                
                mongo_db_manager.DBManager().update_user_category(user, category_type, amount)

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
