import categories
from handlers.categories_settings.category_settings import CategorySettingsCreator, CategorySettings


class PeopleSettingsCreator(CategorySettingsCreator):
    def factory_method(self) -> CategorySettings:
        return PeopleSettings()

class PeopleSettings(CategorySettings):
    PEOPLE_CARD_SETTINGS_CHECK_BTN_ID = "people_check_btn"
    PEOPLE_WORD_AMOUNT_BTN_ID = "word_amount_people_btn"
    PEOPLE_PLUS_BTN_ID = "people_plus_btn"
    PEOPLE_MINUS_BTN_ID = "people_minus_btn"

    people_amount_key = "people_amount"
    people_chosen_key = "people_chosen"
    people_no_chosen_key = "people_no_chosen"
    
    def get_category_name_rus(self) -> str:
        return categories.People.CATEGORY_NAME_RUS
    
    def get_category_icon(self) -> str:
        return categories.People.ICON
    
    def get_card_settings_check_btn_id(self):
        return self.PEOPLE_CARD_SETTINGS_CHECK_BTN_ID
    
    def get_word_amount_btn_id(self):
        return self.PEOPLE_WORD_AMOUNT_BTN_ID
    
    def get_plus_btn_id(self):
        return self.PEOPLE_PLUS_BTN_ID
    
    def get_minus_btn_id(self):
        return self.PEOPLE_MINUS_BTN_ID
    
    def get_amount_key(self):
        return self.people_amount_key
    
    def get_chosen_key(self):
        return self.people_chosen_key
    
    def get_no_chosen_key(self):
        return self.people_no_chosen_key