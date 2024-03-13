import asyncio
from typing import Dict, Any
from db.mongo import mongo_db_manager

from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram import types

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Checkbox, Start, Row, Cancel

from handlers import card_settings_menu

router = Router()
router.include_router(card_settings_menu.router)


class Settings(StatesGroup):
    START = State()


ROLL_DICE_BTN_ID = "dice"
CARD_SETTINGS_BTN_ID = "card_settings"
SAVE_SETTINGS_BTN_ID = "save_settings"


async def on_dialog_start(start_data: Any, dialog_manager: DialogManager):
    user = mongo_db_manager.DBManager().get_user(dialog_manager.event.from_user.id)

    dialog_manager.dialog_data["roll_dice"] = user.roll_dice
    dialog_manager.dialog_data["no_roll_dice"] = not user.roll_dice


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "roll_dice": dialog_manager.dialog_data["roll_dice"],
        "no_roll_dice": dialog_manager.dialog_data["no_roll_dice"],
    }


async def save_main_settings(
    callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager
):
    mongo_db_manager.DBManager().update_user(callback.from_user.id, 
                                             dialog_manager.find(ROLL_DICE_BTN_ID).is_checked())
    dump = await callback.message.answer("Настройки сохранены!")
    await callback.answer()

    await asyncio.sleep(5)
    try:
        await dump.delete()
    except Exception as e:
        pass

settings = Dialog(
    Window(
        Const("Настройки"),
        Checkbox(
            checked_text=Const("[✓] Бросать кубик 🎲"),
            unchecked_text=Const("[✗] Бросать кубик 🎲"),
            id=ROLL_DICE_BTN_ID,
            default=True,
            when="roll_dice",
        ),
        Checkbox(
            checked_text=Const("[✓] Бросать кубик 🎲"),
            unchecked_text=Const("[✗] Бросать кубик 🎲"),
            id=ROLL_DICE_BTN_ID,
            default=False,
            when="no_roll_dice",
        ),
        Start(
            Const("Настройки карточки"),
            id=CARD_SETTINGS_BTN_ID,
            state=card_settings_menu.UpdateCardSettings.START
        ),
        Row(
            Cancel(text=Const("Выход")),
            Cancel(
                text=Const("Сохранить"), id=SAVE_SETTINGS_BTN_ID, on_click=save_main_settings
            ),
        ),
        state=Settings.START,
    ),
    on_start=on_dialog_start,
    getter=getter,
)

router.include_router(settings)
