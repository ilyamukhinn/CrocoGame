from aiogram import types

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

words_amount_key = "words_amount"

def amount_changed(
    button: Button, dialog_manager: DialogManager,
    button_minus_id: str, button_plus_id: str, check_button_id: str,
    amount_key: str
):
    if button.widget_id == button_minus_id and dialog_manager.dialog_data[amount_key] != 0:
        dialog_manager.dialog_data[amount_key] -= 1
        if dialog_manager.find(check_button_id).is_checked():
            dialog_manager.dialog_data[words_amount_key] -= 1
    if button.widget_id == button_plus_id and dialog_manager.dialog_data[amount_key] != 6:
        dialog_manager.dialog_data[amount_key] += 1
        if dialog_manager.find(check_button_id).is_checked():
            dialog_manager.dialog_data[words_amount_key] += 1


    