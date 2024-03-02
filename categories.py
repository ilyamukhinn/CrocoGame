import random
from typing import Union
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Films:
    ICON = "🎬"
    CATEGORY_NAME_RUS = "Фильмы"
    CATEGORY_NAME_ENG = "Films"
    FILENAME: str = os.path.join(ROOT_DIR, "data", "films")

    def __init__(self):
        self.films = self.read_films_from_file()

    def read_films_from_file(self) -> list[str]:
        with open(Films.FILENAME, "r", encoding="utf-8") as file:
            return list(line.strip() for line in file.readlines())

    def get_films_sample(self, sample_size: int) -> list[str]:
        return random.sample(self.films, sample_size)


class People:
    ICON = "⭐️"
    CATEGORY_NAME_RUS = "Личности"
    CATEGORY_NAME_ENG = "People"
    FILENAME = os.path.join(ROOT_DIR, "data", "people")

    def __init__(self):
        self.people = self.read_people_from_file()

    def read_people_from_file(self) -> list[str]:
        with open(People.FILENAME, "r", encoding="utf-8") as file:
            return list(line.strip() for line in file.readlines())

    def get_people_sample(self, sample_size: int) -> list[str]:
        return random.sample(self.people, sample_size)


class Books:
    ICON = "📚"
    CATEGORY_NAME_RUS = "Книги"
    CATEGORY_NAME_ENG = "Books"
    FILENAME = os.path.join(ROOT_DIR, "data", "books")

    def __init__(self):
        self.books = self.read_books_from_file()

    def read_books_from_file(self) -> list[str]:
        with open(Books.FILENAME, "r", encoding="utf-8") as file:
            return list(line.strip() for line in file.readlines())

    def get_books_sample(self, sample_size: int) -> list[str]:
        return random.sample(self.books, sample_size)


class Statements:
    ICON = "💭"
    CATEGORY_NAME_RUS = "Высказывания"
    CATEGORY_NAME_ENG = "Statements"
    FILENAME = os.path.join(ROOT_DIR, "data", "statements")

    def __init__(self):
        self.statements = self.read_statements_from_file()

    def read_statements_from_file(self) -> list[str]:
        with open(Statements.FILENAME, "r", encoding="utf-8") as file:
            return list(line.strip() for line in file.readlines())

    def get_statements_sample(self, sample_size: int) -> list[str]:
        return random.sample(self.statements, sample_size)


categories_types = [Films, People, Books, Statements]
