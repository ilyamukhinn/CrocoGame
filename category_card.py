from categories import Films, Books, People, Statements, _categories_types
from abc import ABC, abstractmethod
import categories

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
        category_desc = " ".join([Films.ICON, Films.CATEGORY_NAME_RUS, "\n"])

        for word in Films().get_films_sample(self.sample_size):
            counter += 1
            category_desc += "({}) ".format(counter) + " ".join([word, "\n"])
        
        return "".join([category_desc, self.component.get_category_sample(counter)])


class BooksDecorator(Decorator):
    def get_category_sample(self, counter: int = 0) -> str:
        category_desc = " ".join([Books.ICON, Books.CATEGORY_NAME_RUS, "\n"])

        for word in Books().get_books_sample(self.sample_size):
            counter += 1
            category_desc += "({}) ".format(counter) + " ".join([word, "\n"])
        
        return "".join([category_desc, self.component.get_category_sample(counter)])
    
class PeopleDecorator(Decorator):
    def get_category_sample(self, counter: int = 0) -> str:
        category_desc = " ".join([People.ICON, People.CATEGORY_NAME_RUS, "\n"])

        for word in People().get_people_sample(self.sample_size):
            counter += 1
            category_desc += "({}) ".format(counter) + " ".join([word, "\n"])
        
        return "".join([category_desc, self.component.get_category_sample(counter)])


class StatementsDecorator(Decorator):
    def get_category_sample(self, counter: int = 0) -> str:
        category_desc = " ".join([Statements.ICON, Statements.CATEGORY_NAME_RUS, "\n"])

        for word in Statements().get_statements_sample(self.sample_size):
            counter += 1
            category_desc += "({}) ".format(counter) + " ".join([word, "\n"])
        
        return "".join([category_desc, self.component.get_category_sample(counter)])


class card():
    _categories_info: dict[_categories_types: int] = None
    _roll_dice: int = None

    @property
    def categories_info(self) -> dict[_categories_types: int]:
        return self._categories_info
    
    @property
    def roll_dice(self) -> int:
        return self._roll_dice

    def gen_game_card(self, user_id: int) -> tuple[str, int]:
        self._categories_info, self._roll_dice = self._get_user_info(user_id)
        base_component: BaseComponent = BaseComponent()
        latest_decorator: Decorator = Decorator(base_component, 0)

        for category_type, words_amount in self.categories_info.items():
            match category_type:
                case categories.Films:
                    latest_decorator = FilmsDecorator(latest_decorator, words_amount)
                case categories.Books:
                    latest_decorator = BooksDecorator(latest_decorator, words_amount)
                case categories.People:
                    latest_decorator = PeopleDecorator(latest_decorator, words_amount)
                case categories.Statements:
                    latest_decorator = StatementsDecorator(latest_decorator, words_amount)

        return latest_decorator.get_category_sample(), self.roll_dice

    def _get_user_info(self, user_id: int) -> tuple[dict[_categories_types: int], int]:
        return {
            Films: 2,
            People: 3,
            Books: 1,
            Statements: 4
        }, 1




if __name__ == "__main__":
    for item in card().gen_game_card(1):
        print(item)