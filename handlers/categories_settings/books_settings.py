from models import book_model
from handlers.categories_settings.category_settings import CategorySettingsCreator, CategorySettings

class BooksSettingsCreator(CategorySettingsCreator):
    def factory_method(self) -> CategorySettings:
        return BooksSettings()


class BooksSettings(CategorySettings):
    BOOKS_CARD_SETTINGS_CHECK_BTN_ID = "books_check_btn"
    BOOKS_WORD_AMOUNT_BTN_ID = "word_amount_books_btn"
    BOOKS_PLUS_BTN_ID = "books_plus_btn"
    BOOKS_MINUS_BTN_ID = "books_minus_btn"

    books_amount_key = "books_amount"
    books_chosen_key = "books_chosen"
    books_no_chosen_key = "books_no_chosen"
    
    def get_category_name_eng(self) -> str:
        return book_model.Book.AdditionalData.CATEGORY_NAME_ENG

    def get_category_name_rus(self) -> str:
        return book_model.Book.AdditionalData.CATEGORY_NAME_RUS
    
    def get_category_icon(self) -> str:
        return book_model.Book.AdditionalData.ICON
    
    def get_card_settings_check_btn_id(self):
        return self.BOOKS_CARD_SETTINGS_CHECK_BTN_ID
    
    def get_word_amount_btn_id(self):
        return self.BOOKS_WORD_AMOUNT_BTN_ID
    
    def get_plus_btn_id(self):
        return self.BOOKS_PLUS_BTN_ID
    
    def get_minus_btn_id(self):
        return self.BOOKS_MINUS_BTN_ID
    
    def get_amount_key(self):
        return self.books_amount_key
    
    def get_chosen_key(self):
        return self.books_chosen_key
    
    def get_no_chosen_key(self):
        return self.books_no_chosen_key

