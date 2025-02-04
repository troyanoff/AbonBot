from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def company_repr_inline(i18n: dict, one_company: bool):
    kb_builder = InlineKeyboardBuilder()
    kb_buttons: list[InlineKeyboardButton] = []
    if not one_company:
        kb_buttons.append(
            InlineKeyboardButton(
                text=i18n['buttons']['back'],
                callback_data='back'
            )
        )
        kb_buttons.append(
            InlineKeyboardButton(
                text=i18n['buttons']['forward'],
                callback_data='forward'
            )
        )
        kb_builder.row(*kb_buttons, width=2)
    kb_builder.row(InlineKeyboardButton(
        text=i18n['buttons']['manage_company'],
        callback_data='manage_company'
    ))
    kb_builder.row(InlineKeyboardButton(
        text=i18n['buttons']['create_company'],
        callback_data='create_company'
    ))
    kb_builder.row(InlineKeyboardButton(
        text=i18n['buttons']['cancel'],
        callback_data='cancel'
    ))
    return kb_builder.as_markup()
