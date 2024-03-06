import categories
from handlers.categories_settings.category_settings import CategorySettingsCreator, CategorySettings

class FilmsSettingsCreator(CategorySettingsCreator):
    def factory_method(self) -> CategorySettings:
        return FilmsSettings()

class FilmsSettings(CategorySettings):
    FILMS_CARD_SETTINGS_CHECK_BTN_ID = "films_check_btn"
    FILMS_WORD_AMOUNT_BTN_ID = "word_amount_films_btn"
    FILMS_PLUS_BTN_ID = "films_plus_btn"
    FILMS_MINUS_BTN_ID = "films_minus_btn"

    films_amount_key = "films_amount"
    films_chosen_key = "films_chosen"
    films_no_chosen_key = "films_no_chosen"

    def get_category_name_rus(self) -> str:
        return categories.Films.CATEGORY_NAME_RUS
    
    def get_category_icon(self) -> str:
        return categories.Films.ICON

    def get_card_settings_check_btn_id(self) -> str:
        return self.FILMS_CARD_SETTINGS_CHECK_BTN_ID
    
    def get_word_amount_btn_id(self) -> str:
        return self.FILMS_WORD_AMOUNT_BTN_ID
    
    def get_plus_btn_id(self) -> str:
        return self.FILMS_PLUS_BTN_ID
    
    def get_minus_btn_id(self) -> str:
        return self.FILMS_MINUS_BTN_ID
    
    def get_amount_key(self) -> str:
        return self.films_amount_key
    
    def get_chosen_key(self) -> str:
        return self.films_chosen_key
    
    def get_no_chosen_key(self) -> str:
        return self.films_no_chosen_key

