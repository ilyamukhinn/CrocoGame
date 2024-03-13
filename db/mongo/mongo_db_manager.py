from pymodm import connect
from config_reader import config
from models import (
    film_model, 
    book_model, 
    character_model, 
    statement_model,
    category_model,
    user_model,
    user_category_model)

class DBManager():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBManager, cls).__new__(cls)
            cls.instance.init()
        return cls.instance


    def init(self):
        connect(config.mongo_url.get_secret_value())

    ######################################################

    def create_films_collection(self) -> None:
        films_list: list[str]
        with open(film_model.Film.AdditionalData.FILENAME, "r", encoding="utf-8") as file:
            films_list = list(line.strip() for line in file.readlines())

        for f in films_list:
            try:
                film_model.Film.objects.get({'name': f})
            except film_model.Film.DoesNotExist:
                film_model.Film(name=f).save()

    def get_films_sample(self, sample_size: int) -> list[film_model.Film]:
        return [film_model.Film(name=film['name']) for film in film_model.Film.objects.raw({}).aggregate(
            {"$sample": {"size": sample_size}}
            )]

    def create_books_collection(self) -> None:
        books_list: list[str]
        with open(book_model.Book.AdditionalData.FILENAME, "r", encoding="utf-8") as file:
            books_list = list(line.strip() for line in file.readlines())

        for f in books_list:
            try:
                book_model.Book.objects.get({'name': f})
            except book_model.Book.DoesNotExist:
                book_model.Book(name=f).save()
    def get_books_sample(self, sample_size: int) -> list[any]:
        return [book_model.Book(name=book['name']) for book in book_model.Book.objects.raw({}).aggregate(
            {"$sample": {"size": sample_size}}
            )]

    def create_characters_collection(self) -> None:
        characters_list: list[str]
        with open(character_model.Character.AdditionalData.FILENAME, "r", encoding="utf-8") as file:
            characters_list = list(line.strip() for line in file.readlines())

        for f in characters_list:
            try:
                character_model.Character.objects.get({'name': f})
            except character_model.Character.DoesNotExist:
                character_model.Character(name=f).save()
    
    def get_characters_sample(self, sample_size: int) -> list[any]:
        return [character_model.Character(name=character['name']) for character in character_model.Character.objects.raw({}).aggregate(
            {"$sample": {"size": sample_size}}
            )]

    def create_statements_collection(self) -> None:
        statements_list: list[str]
        with open(statement_model.Statement.AdditionalData.FILENAME, "r", encoding="utf-8") as file:
            statements_list = list(line.strip() for line in file.readlines())

        for f in statements_list:
            try:
                statement_model.Statement.objects.get({'name': f})
            except statement_model.Statement.DoesNotExist:
                statement_model.Statement(name=f).save()
        
    def get_statements_sample(self, sample_size: int) -> list[any]:
        return [statement_model.Statement(name=statement['name']) for statement in statement_model.Statement.objects.raw({}).aggregate(
            {"$sample": {"size": sample_size}}
            )]


    ######################################################

    def create_categories_collection(self) -> None:
        for c in [
            film_model.Film.AdditionalData.CATEGORY_NAME_ENG,
            book_model.Book.AdditionalData.CATEGORY_NAME_ENG,
            statement_model.Statement.AdditionalData.CATEGORY_NAME_ENG,
            character_model.Character.AdditionalData.CATEGORY_NAME_ENG]:
            try:
                category_model.Category.objects.get({'name': c})
            except category_model.Category.DoesNotExist:
                category_model.Category(name=c).save()

    def get_category(self, category_name: str) -> category_model.Category | None:
        try:
            return category_model.Category.objects.get({'name': category_name})
        except category_model.Category.DoesNotExist:
            return None
    
    def get_all_categories(self) -> list[category_model.Category] | None:
        try:
            return list(category_model.Category.objects.raw({}))
        except category_model.Category.DoesNotExist:
            return None

    ######################################################

    def get_user(self, user_id: int) -> user_model.User | None:
        try:
            return user_model.User.objects.get({'_id': user_id})
        except user_model.User.DoesNotExist:
            return None

    def insert_user(self, user_id: int, roll_dice: bool = True) -> None:
        try:
            user_model.User.objects.get({'_id': user_id})
        except user_model.User.DoesNotExist:
            user_model.User(user_id, roll_dice).save()

    def update_user(self, user_id: int, roll_dice: bool) -> None:
        user_model.User.objects.raw({"_id": user_id}).update( # get -> raw
            {"$set": {"roll_dice": roll_dice}}
        )

    def remove_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        user.delete()

    ######################################################

    def get_user_category(self, user: user_model.User, category: category_model.Category) -> user_category_model.UserCategory | None:
        try:
            return user_category_model.UserCategory.objects.get({'user': user.pk, 'category': category.pk})
        except user_category_model.UserCategory.DoesNotExist:
            return None
        
    def get_user_categories(self, user_id: int) -> list[user_category_model.UserCategory] | None:
        try:
            return list(user_category_model.UserCategory.objects.raw({'user': user_id}))
        except user_category_model.UserCategory.DoesNotExist:
            return None

    def insert_user_category(self, user: user_model.User, category: category_model.Category, amount: int) -> None:
        try:
            user_category_model.UserCategory.objects.get({'user': user.pk, 'category': category.pk})
        except user_category_model.UserCategory.DoesNotExist:
            user_category_model.UserCategory(user=user, category=category, amount=amount).save()

    def update_user_category(self, user: user_model.User, category: category_model.Category, amount: int) -> None:
        user_category_model.UserCategory.objects.raw({'user': user.pk, 'category': category.pk}).update( # get -> raw
            {"$set": {"amount": amount}}
        )

    