from abc import ABC, abstractmethod
import random

from db.mongo import mongo_db_manager
from models import (
    film_model, 
    book_model, 
    character_model, 
    statement_model)

class Component(ABC):
    @abstractmethod
    def get_category_sample(self, counter: int = 0) -> str:
        pass


class BaseComponent(Component):
    def get_category_sample(self, counter: int = 0) -> str:
        return ""


class Decorator(Component):
    _component: Component = None
    _sample_size: int = None

    def __init__(self, component: Component, sample_size: int) -> None:
        self._component = component
        self._sample_size = sample_size

    @property
    def component(self) -> Component:
        return self._component
    
    @property
    def sample_size(self) -> int:
        return self._sample_size

    def get_category_sample(self, counter: int = 0) -> str:
        return self._component.get_category_sample(counter)


class FilmsDecorator(Decorator):
    def get_category_sample(self, counter: int = 0) -> str:
        category_desc = " ".join([film_model.Film.AdditionalData.ICON, 
                                  film_model.Film.AdditionalData.CATEGORY_NAME_RUS, "\n"])

        for film in mongo_db_manager.DBManager().get_films_sample(self.sample_size):
            counter += 1
            category_desc += "({}) ".format(counter) + " ".join([film.name, "\n"])
        
        return "".join([category_desc, self.component.get_category_sample(counter)])


class BooksDecorator(Decorator):
    def get_category_sample(self, counter: int = 0) -> str:
        category_desc = " ".join([book_model.Book.AdditionalData.ICON, 
                                  book_model.Book.AdditionalData.CATEGORY_NAME_RUS, "\n"])

        for book in mongo_db_manager.DBManager().get_books_sample(self.sample_size):
            counter += 1
            category_desc += "({}) ".format(counter) + " ".join([book.name, "\n"])
        
        return "".join([category_desc, self.component.get_category_sample(counter)])
    
class CharacterDecorator(Decorator):
    def get_category_sample(self, counter: int = 0) -> str:
        category_desc = " ".join([character_model.Character.AdditionalData.ICON, 
                                  character_model.Character.AdditionalData.CATEGORY_NAME_RUS, "\n"])

        for character in mongo_db_manager.DBManager().get_characters_sample(self.sample_size):
            counter += 1
            category_desc += "({}) ".format(counter) + " ".join([character.name, "\n"])
        
        return "".join([category_desc, self.component.get_category_sample(counter)])


class StatementsDecorator(Decorator):
    def get_category_sample(self, counter: int = 0) -> str:
        category_desc = " ".join([statement_model.Statement.AdditionalData.ICON, 
                                  statement_model.Statement.AdditionalData.CATEGORY_NAME_RUS, "\n"])

        for statement in mongo_db_manager.DBManager().get_statements_sample(self.sample_size):
            counter += 1
            category_desc += "({}) ".format(counter) + " ".join([statement.name, "\n"])
        
        return "".join([category_desc, self.component.get_category_sample(counter)])


class card():
    _categories_info: dict[str: int] = None
    _roll_dice: int = None

    @property
    def categories_info(self) -> dict[str: int]:
        return self._categories_info
    
    @property
    def roll_dice(self) -> int:
        return self._roll_dice

    def gen_game_card(self, user_id: int) -> tuple[str, int]:
        self._categories_info, self._roll_dice = self._get_user_info(user_id)
        base_component: BaseComponent = BaseComponent()
        latest_decorator: Decorator = Decorator(base_component, 0)

        for category_type, words_amount in sorted(self.categories_info.items(), key=lambda x: random.random()):
            if words_amount == 0:
                continue
            match category_type:
                case film_model.Film.AdditionalData.CATEGORY_NAME_ENG:
                    latest_decorator = FilmsDecorator(latest_decorator, words_amount)
                case book_model.Book.AdditionalData.CATEGORY_NAME_ENG:
                    latest_decorator = BooksDecorator(latest_decorator, words_amount)
                case character_model.Character.AdditionalData.CATEGORY_NAME_ENG:
                    latest_decorator = CharacterDecorator(latest_decorator, words_amount)
                case statement_model.Statement.AdditionalData.CATEGORY_NAME_ENG:
                    latest_decorator = StatementsDecorator(latest_decorator, words_amount)

        return latest_decorator.get_category_sample(), self.roll_dice

    def _get_user_info(self, user_id: int) -> tuple[dict[str: int], int]:
        user_categories = mongo_db_manager.DBManager().get_user_categories(user_id)
        return {user_category.category.name: user_category.amount for user_category in user_categories}, 1

if __name__ == "__main__":
    for item in card().gen_game_card(379340519):
        print(item)