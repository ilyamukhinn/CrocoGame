from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod

from aiogram import types

from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Checkbox, ManagedCheckbox

class CategorySettingsCreator(ABC):
    words_amount_key = "words_amount"

    @abstractmethod
    def factory_method(self):
        pass

    def amount_changed(
        self, button: Button, dialog_manager: DialogManager,
        button_minus_id: str, button_plus_id: str, check_button_id: str,
        amount_key: str
    ):
        if button.widget_id == button_minus_id and dialog_manager.dialog_data[amount_key] != 0:
            dialog_manager.dialog_data[amount_key] -= 1
            if dialog_manager.find(check_button_id).is_checked():
                dialog_manager.dialog_data[self.words_amount_key] -= 1
        if button.widget_id == button_plus_id and dialog_manager.dialog_data[amount_key] != 6:
            dialog_manager.dialog_data[amount_key] += 1
            if dialog_manager.find(check_button_id).is_checked():
                dialog_manager.dialog_data[self.words_amount_key] += 1

    async def category_amount_changed(
        self, callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager
    ):
        category = self.factory_method()
        self.amount_changed(
            button, dialog_manager, 
            category.get_minus_btn_id(), category.get_plus_btn_id(), category.get_card_settings_check_btn_id(),
            category.get_amount_key())
        await callback.answer()
        return

    async def category_check_changed(
        self, event: ChatEvent, checkbox: ManagedCheckbox, dialog_manager: DialogManager
    ):
        if checkbox.is_checked():
            dialog_manager.dialog_data[self.words_amount_key] += \
                self.get_category_amount(dialog_manager)
        else:
            dialog_manager.dialog_data[self.words_amount_key] -= \
                self.get_category_amount(dialog_manager)

    def getter(self, dialog_manager: DialogManager) -> dict[str, Any]:
        category = self.factory_method()
        return {
            category.get_chosen_key(): dialog_manager.dialog_data[category.get_chosen_key()],
            category.get_no_chosen_key(): dialog_manager.dialog_data[category.get_no_chosen_key()],
            category.get_amount_key(): dialog_manager.dialog_data[category.get_amount_key()],
        }
    
    def get_if_category_chosen(self, dialog_manager: DialogManager) -> bool:
        category = self.factory_method()
        return dialog_manager.find(category.get_card_settings_check_btn_id()).is_checked()

    def get_category_amount(self, dialog_manager: DialogManager) -> int:
        category = self.factory_method()
        return dialog_manager.dialog_data[category.get_amount_key()]

    def get_category_amount_if_chosen(self, dialog_manager: DialogManager) -> int:
        category = self.factory_method()
        return dialog_manager.dialog_data[category.get_amount_key()] if \
            dialog_manager.find(category.get_card_settings_check_btn_id()).is_checked() else 0

    def get_current_category_settings(self, dialog_manager: DialogManager) -> str:
        category = self.factory_method()
        return "• {0} {1} [{2}], слов: {3}".format(
            category.get_category_icon(), 
            category.get_category_name_rus(),
            "✓" if self.get_if_category_chosen(dialog_manager) else "✗",
            self.get_category_amount(dialog_manager))

    def category_group_creator(self) -> list[Any]:
        category = self.factory_method()
        return [
            Checkbox(
                checked_text=Const("[✓] {} {}".format(category.get_category_name_rus(), category.get_category_icon())),
                unchecked_text=Const("[✗] {} {}".format(category.get_category_name_rus(), category.get_category_icon())),
                id=category.get_card_settings_check_btn_id(),
                default=True,
                when=category.get_chosen_key(),
                on_state_changed=self.category_check_changed
            ),
            Checkbox(
                checked_text=Const("[✓] {} {}".format(category.get_category_name_rus(), category.get_category_icon())),
                unchecked_text=Const("[✗] {} {}".format(category.get_category_name_rus(), category.get_category_icon())),
                id=category.get_card_settings_check_btn_id(),
                default=False,
                when=category.get_no_chosen_key(),
                on_state_changed=self.category_check_changed
            ),
            Button(text=Format("Выбрано слов: {{dialog_data[{0}]}}".format(category.get_amount_key())), id=category.get_word_amount_btn_id()),
            Button(text=Const("-"), id=category.get_minus_btn_id(), on_click=self.category_amount_changed),
            Button(text=Const("+"), id=category.get_plus_btn_id(), on_click=self.category_amount_changed)
        ]
    
    def get_category_name_eng(self) -> str:
        return self.factory_method().get_category_name_eng()
    
    def get_category_name_rus(self) -> str:
        return self.factory_method().get_category_name_rus()
    
    def get_category_icon(self) -> str:
        return self.factory_method().get_category_icon()

    def get_card_settings_check_btn_id(self) -> str:
        return self.factory_method().get_card_settings_check_btn_id()
    
    def get_word_amount_btn_id(self) -> str:
        return self.factory_method().get_word_amount_btn_id()
    
    def get_plus_btn_id(self) -> str:
        return self.factory_method().get_plus_btn_id()
    
    def get_minus_btn_id(self) -> str:
        return self.factory_method().get_minus_btn_id()
    
    def get_amount_key(self) -> str:
        return self.factory_method().get_amount_key()
    
    def get_chosen_key(self) -> str:
        return self.factory_method().get_chosen_key()
    
    def get_no_chosen_key(self) -> str:
        return self.factory_method().get_no_chosen_key()

class CategorySettings(ABC):
    @abstractmethod
    def get_category_name_eng(self) -> str:
        pass

    @abstractmethod
    def get_category_name_rus(self) -> str:
        pass
    
    @abstractmethod
    def get_category_icon(self) -> str:
        pass
    
    @abstractmethod
    def get_card_settings_check_btn_id(self) -> str:
        pass

    @abstractmethod
    def get_word_amount_btn_id(self) -> str:
        pass

    @abstractmethod
    def get_plus_btn_id(self) -> str:
        pass

    @abstractmethod
    def get_minus_btn_id(self) -> str:
        pass

    @abstractmethod
    def get_amount_key(self) -> str:
        pass

    @abstractmethod
    def get_chosen_key(self) -> str:
        pass

    @abstractmethod
    def get_no_chosen_key(self) -> str:
        pass

