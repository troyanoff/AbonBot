from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def kb_create_client_start(_buttons: dict):
    button = KeyboardButton(text=_buttons['client_create'])

    kb_builder = ReplyKeyboardBuilder()

    kb_builder.row(button)

    return kb_builder.as_markup(
        one_time_keyboard=True,
        resize_keyboard=True
    )
