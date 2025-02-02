from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_inline_kb(
    buttons: dict,
    width: int,
    *args: str,
    cancel_button: bool = True,
    **kwargs: str
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            kb_buttons.append(InlineKeyboardButton(
                text=buttons[button] if button in buttons else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            kb_buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*kb_buttons, width=width)
    if cancel_button:
        kb_builder.row(InlineKeyboardButton(
            text=buttons['cancel'],
            callback_data='cancel'
        ))

    return kb_builder.as_markup()