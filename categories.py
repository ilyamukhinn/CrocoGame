import random


class Category:
    def _remove_duplicates(self, filename: str) -> None:
        items = set(line.strip() for line in open(filename))
        with open(filename, "w") as f:
            f.writelines("%s\n" % item for item in items)

    def _read_items_from_file(self, filename: str) -> list[str]:
        with open(filename, "r", encoding="utf-8") as file:
            return list(line.strip() for line in file.readlines())

    def _get_items_sample(self, items: list[str], sample_size: int) -> list[str]:
        return random.sample(items, sample_size)


class Films(Category):
    ICON = "🎬"
    CATEGORY_NAME = "Фильмы"
    CATEGORY_NAME_ENG = "Films"

    def __init__(self, filename: str = "data/films"):
        self.filename = filename
        self.films = self.read_films_from_file()

    def remove_films_duplicates(self, filename: str = "") -> None:
        super()._remove_duplicates(filename if filename else self.filename)

    def read_films_from_file(self, filename: str = "") -> list[str]:
        return super()._read_items_from_file(filename if filename else self.filename)

    def get_films_sample(self, sample_size: int) -> list[str]:
        return super()._get_items_sample(self.films, sample_size)


class People(Category):
    ICON = "⭐️"
    CATEGORY_NAME = "Личности"
    CATEGORY_NAME_ENG = "People"

    def __init__(self, filename: str = "data/people"):
        self.filename = filename
        self.people = self.read_people_from_file()

    def remove_people_duplicates(self, filename: str = "") -> None:
        super()._remove_duplicates(filename if filename else self.filename)

    def read_people_from_file(self, filename: str = "") -> list[str]:
        return super()._read_items_from_file(filename if filename else self.filename)

    def get_people_sample(self, sample_size: int) -> list[str]:
        return super()._get_items_sample(self.people, sample_size)


class Books(Category):
    ICON = "📚"
    CATEGORY_NAME = "Произведения литературы"
    CATEGORY_NAME_ENG = "Books"

    def __init__(self, filename: str = "data/books"):
        self.filename = filename
        self.books = self.read_books_from_file()

    def remove_books_duplicates(self, filename: str = "") -> None:
        super()._remove_duplicates(filename if filename else self.filename)

    def read_books_from_file(self, filename: str = "") -> list[str]:
        return super()._read_items_from_file(filename if filename else self.filename)

    def get_books_sample(self, sample_size: int) -> list[str]:
        return super()._get_items_sample(self.books, sample_size)


class Categories:
    categories_list: list[Category] = [Films, People, Books]
