import card

from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji

from aiogram_dialog import DialogManager

from middlewares import long_operation_action_middlware
from keyboards import main_menu_reply_keyboard
from handlers import settings_menu
from db.mongo import mongo_db_manager

from models import (
    film_model, 
    book_model, 
    character_model, 
    statement_model)

from config_reader import config

router = Router()
router.include_routers(settings_menu.router)
router.callback_query.outer_middleware(
    long_operation_action_middlware.ChatActionMiddleware()
)

def register_user(user_id: int) -> None:
    mongo_db_manager.DBManager().insert_user(user_id)

    for index, c in enumerate([
        film_model.Film.AdditionalData.CATEGORY_NAME_ENG,
        book_model.Book.AdditionalData.CATEGORY_NAME_ENG,
        statement_model.Statement.AdditionalData.CATEGORY_NAME_ENG,
        character_model.Character.AdditionalData.CATEGORY_NAME_ENG]):
        category = mongo_db_manager.DBManager().get_category(c)
        user = mongo_db_manager.DBManager().get_user(user_id)
        mongo_db_manager.DBManager().insert_user_category(user, category, 2 if index < 3 else 0)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    register_user(message.from_user.id)
    await message.answer(
        text="Привет! Меня зовут Филипп, и я могу помочь тебе "
        "отдохнуть от рабочих будней, ты можешь сыграть со "
        'мной в игру "Крокодил"🐊\n'
        "Чтобы узнать подробней о моих возможностях, перейди "
        "в меню и выбери команду /help или нажми на неё прямо "
        "здесь!",
        reply_markup=main_menu_reply_keyboard.make_start_menu_keyboard_builder().as_markup(
            resize_keyboard=True
        ),
    )


@router.message(
    F.text.lower() == "получить карточку 🃏", flags={"long_operation": "typing"}
)
@router.message(Command("get_card"), flags={"long_operation": "typing"})
async def cmd_get_game_card(
    message: types.Message
):
    card_data_text, roll_dice = card.card().gen_game_card(message.from_user.id)
    await message.answer(text=card_data_text)
    if roll_dice:
        await message.answer_dice(emoji=DiceEmoji.DICE)


@router.message(F.text.lower() == "настройки ⚙️")
@router.message(Command("settings"))
async def cmd_settings(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(settings_menu.Settings.START)

@router.message(F.text.lower() == "бросить кубик 🎲")
async def cmd_settings(message: types.Message, dialog_manager: DialogManager):
    await message.answer_dice(emoji=DiceEmoji.DICE)

@router.message(F.text.lower() == "помощь ℹ️")
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(text="Здесь будет справка о приложении")


@router.message(F.text.lower() == "правила игры ⚖️")
@router.message(Command("rules"))
async def cmd_rules(message: types.Message):
    await message.answer(text="Здесь будет справка о правилах игры")


@router.message(F.text)
async def cmd_missing(message: types.Message):
    await message.answer(text="Не знаю такой команды :(")
