from typing import Any
import categories
from handlers.categories import settings_category_amount_change
from handlers.categories.category_settings import CategorySettingsCreator, CategorySettings

from aiogram import types

from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Checkbox, ManagedCheckbox

class StatementsSettingsCreator(CategorySettingsCreator):
    def factory_method(self) -> CategorySettings:
        return StatementsSettings()

class StatementsSettings(CategorySettings):
    STATEMENTS_CARD_SETTINGS_CHECK_BTN_ID = "statements_check_btn"
    STATEMENTS_WORD_AMOUNT_BTN_ID = "word_amount_statements_btn"
    STATEMENTS_PLUS_BTN_ID = "statements_plus_btn"
    STATEMENTS_MINUS_BTN_ID = "statements_minus_btn"

    statements_amount_key = "statements_amount"
    statements_chosen_key = "statements_chosen"
    statements_no_chosen_key = "statements_no_chosen"
    
    def get_category_name_rus(self) -> str:
        return categories.Statements.CATEGORY_NAME_RUS
    
    def get_category_icon(self) -> str:
        return categories.Statements.ICON
    
    def get_card_settings_check_btn_id(self):
        return self.STATEMENTS_CARD_SETTINGS_CHECK_BTN_ID
    
    def get_word_amount_btn_id(self):
        return self.STATEMENTS_WORD_AMOUNT_BTN_ID
    
    def get_plus_btn_id(self):
        return self.STATEMENTS_PLUS_BTN_ID
    
    def get_minus_btn_id(self):
        return self.STATEMENTS_MINUS_BTN_ID
    
    def get_amount_key(self):
        return self.statements_amount_key
    
    def get_chosen_key(self):
        return self.statements_chosen_key
    
    def get_no_chosen_key(self):
        return self.statements_no_chosen_key