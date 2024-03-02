import categories
import sqlite3
import random

from db import main_db_interface, user_db_tables


def generate_text(
    data: dict[categories.categories_types, int],
    categories_objects: dict[str, categories.categories_types],
) -> str:
    card: str = ""
    counter: int = 0

    def add_card_info(
        data: dict[categories.categories_types, list[str]],
        category: categories.categories_types,
        counter: int,
        card: str,
    ) -> dict[str, any]:
        if data[category]:
            card += " ".join([category.ICON, category.CATEGORY_NAME_RUS, "\n"])

        for word in data[category]:
            counter += 1
            card += "({}) ".format(counter) + " ".join([word, "\n"])

        return dict({"card": card, "counter": counter})

    for category, sample_size in sorted(data.items(), key=lambda x: random.random()):
        match category:
            case categories.Films:
                data[category] = categories_objects[
                    categories.Films.CATEGORY_NAME_ENG
                ].get_films_sample(sample_size)

            case categories.People:
                data[category] = categories_objects[
                    categories.People.CATEGORY_NAME_ENG
                ].get_people_sample(sample_size)

            case categories.Books:
                data[category] = categories_objects[
                    categories.Books.CATEGORY_NAME_ENG
                ].get_books_sample(sample_size)

            case categories.Statements:
                data[category] = categories_objects[
                    categories.Statements.CATEGORY_NAME_ENG
                ].get_statements_sample(sample_size)

        result: dict[str, any] = add_card_info(data, category, counter, card)
        card = result["card"]
        counter = result["counter"]

    return card


def generate_card(
    id_user: int, categories_objects: dict[str, categories.categories_types]
) -> dict[str, any]:
    conn = sqlite3.connect(user_db_tables.user_db_path)
    data = main_db_interface.DBInterface.select_record(
        conn,
        user_db_tables.UserTable.user_id_field_name,
        id_user,
        user_db_tables.UserTable.table_name,
    )
    user_categories_data = main_db_interface.DBInterface.select_records(
        conn,
        user_db_tables.UserTable.user_id_field_name,
        id_user,
        user_db_tables.UserCategoryTable.table_name,
    )

    input_generate_text_data: dict[categories.categories_types, list[str]] = {}
    for row in user_categories_data:
        category = user_db_tables.CategoryTable.base_data_inverted.get(
            row[user_db_tables.UserCategoryTable.user_category_category_id_field_name],
            0,
        )
        if category:
            input_generate_text_data[category] = row[
                user_db_tables.UserCategoryTable.user_category_category_words_in_card_field_name
            ]

    card_text: str = generate_text(input_generate_text_data, categories_objects)
    data[Card.card_text_field_name] = card_text
    return data


class Card:
    card_text_field_name: str = "card_text"

    words_in_card_field_name: str = "words_in_card"
    words_in_card_field_value: int = 6
    categories_field_name: str = "categories"

    category_chosen_field_name: str = "chosen"
    category_words_in_card_field_name: str = "words_in_card"
    categories_field_values: dict[categories.categories_types, dict[str, int]] = {
        categories.Films: {
            category_chosen_field_name: True,
            category_words_in_card_field_name: 2,
        },
        categories.People: {
            category_chosen_field_name: True,
            category_words_in_card_field_name: 2,
        },
        categories.Books: {
            category_chosen_field_name: True,
            category_words_in_card_field_name: 2,
        },
        categories.Statements: {
            category_chosen_field_name: False,
            category_words_in_card_field_name: 0,
        },
    }
    roll_dice_field_name: str = "roll_dice"
    roll_dice_field_value: int = 1

    BASE_CARD_SETTINGS: dict[str, any] = {
        words_in_card_field_name: words_in_card_field_value,
        roll_dice_field_name: roll_dice_field_value,
        categories_field_name: categories_field_values,
    }

    generate_card = staticmethod(generate_card)
