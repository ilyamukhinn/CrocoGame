import categories

user_db_path = "users_settings.db"


class UserTable:
    table_name: str = "user"

    user_id_field_name: str = "user_id"
    user_id_field_type: str = "INTEGER"
    dice_field_name: str = "roll_dice"
    dice_field_type: int = "INTEGER"
    words_in_card_field_name: str = "words_in_card"
    words_in_card_field_type: str = "INTEGER"

    fields_names_list: list[str] = [
        user_id_field_name,
        dice_field_name,
        words_in_card_field_name,
    ]


class CategoryTable:
    table_name: str = "category"

    category_id_field_name: str = "category_id"
    category_id_field_type: str = "INTEGER"
    category_name_field_name: str = "name"
    category_name_field_type: str = "TEXT"

    fields_names_list: list[str] = [category_id_field_name, category_name_field_name]

    base_data: dict[categories.Category, int] = {
        categories.Films: 1,
        categories.People: 2,
        categories.Books: 3,
    }

    base_data_inverted: dict[int, categories.Category] = {
        1: categories.Films,
        2: categories.People,
        3: categories.Books,
    }


class UserCategoryTable:
    table_name: str = "user_category"

    user_category_user_id_field_name: str = "user_id"
    user_category_user_id_field_type: str = "INTEGER"
    user_category_category_id_field_name: str = "category_id"
    user_category_category_id_field_type: str = "INTEGER"
    user_category_category_chosen_field_name: str = "chosen"
    user_category_category_chosen_field_type: str = "INTEGER"
    user_category_category_words_in_card_field_name: str = "words_in_card"
    user_category_category_words_in_card_field_type: str = "INTEGER"

    fields_names_list: list[str] = [
        user_category_user_id_field_name,
        user_category_category_id_field_name,
        user_category_category_chosen_field_name,
        user_category_category_words_in_card_field_name,
    ]


user_db_tables_names: list[str] = [
    UserTable.table_name,
    CategoryTable.table_name,
    UserCategoryTable.table_name,
]

user_db_tables_full_info: dict[str, dict[str, str]] = {
    UserTable.table_name: {
        UserTable.user_id_field_name: UserTable.user_id_field_type,
        UserTable.dice_field_name: UserTable.dice_field_type,
        UserTable.words_in_card_field_name: UserTable.words_in_card_field_type,
    },
    CategoryTable.table_name: {
        CategoryTable.category_id_field_name: CategoryTable.category_id_field_type,
        CategoryTable.category_name_field_name: CategoryTable.category_name_field_type,
    },
    UserCategoryTable.table_name: {
        UserCategoryTable.user_category_user_id_field_name: UserCategoryTable.user_category_user_id_field_type,
        UserCategoryTable.user_category_category_id_field_name: UserCategoryTable.user_category_category_id_field_type,
        UserCategoryTable.user_category_category_chosen_field_name: UserCategoryTable.user_category_category_chosen_field_type,
        UserCategoryTable.user_category_category_words_in_card_field_name: UserCategoryTable.user_category_category_words_in_card_field_type,
    },
}
