from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang


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


async def create_simply_inline_kb(
    buttons: dict,
    width: int
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_buttons: list[InlineKeyboardButton] = []

    cancel_button = buttons.pop('cancel', None)
    general_button = buttons.pop('general', None)
    for button, value in buttons.items():
        kb_buttons.append(InlineKeyboardButton(
            text=value,
            callback_data=button))

    kb_builder.row(*kb_buttons, width=width)
    if general_button:
        kb_builder.row(InlineKeyboardButton(
            text=general_button,
            callback_data='general'
        ))
    if cancel_button:
        kb_builder.row(InlineKeyboardButton(
            text=cancel_button,
            callback_data='cancel'
        ))
    return kb_builder.as_markup()


async def _forward_sides(data: list[dict], right_side: int):
    len_data = len(data)
    left_side = right_side
    if right_side > len_data - 1:
        left_side = 0
    last_index = len_data - 1
    right_side = left_side + st.default_limit_keyboard_page
    if right_side > last_index:
        right_side = last_index + 1
    return left_side, right_side


async def _back_sides(data: list[dict], left_side: int):
    len_data = len(data)
    limit = st.default_limit_keyboard_page
    if left_side == 0:
        int_pages = (len_data // limit) * limit
        print(int_pages)
        left_side = len_data - limit if int_pages == len_data else int_pages

        right_side = len_data
        return left_side, right_side
    right_side = left_side
    left_side = right_side - limit
    return left_side, right_side


async def create_offset_inline_kb(
    data: list[dict],
    callback_prefix: str,
    side_index: int,
    back: bool,
    lang: str
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_buttons: list[InlineKeyboardButton] = []
    if back:
        left_side, right_side = await _back_sides(
            data=data,
            left_side=side_index
        )
    else:
        left_side, right_side = await _forward_sides(
            data=data,
            right_side=side_index
        )
    for item in data[left_side: right_side]:
        kb_buttons.append(InlineKeyboardButton(
            text=f'{item['num']} {item['name']}',
            callback_data=f'{callback_prefix}:{item['uuid']}'))
    kb_builder.row(*kb_buttons, width=1)
    core_term_lang: core_Lang = getattr(core_term, lang)
    if len(data) > st.default_limit_keyboard_page:
        kb_builder.row(
            InlineKeyboardButton(
                text=core_term_lang.buttons.back,
                callback_data=f'back:{left_side}'
            ),
            InlineKeyboardButton(
                text=core_term_lang.buttons.forward,
                callback_data=f'forward:{right_side}'
            ),
            width=2
        )
    kb_builder.row(
        InlineKeyboardButton(
            text=core_term_lang.buttons.general,
            callback_data='general'
        )
    )
    return kb_builder.as_markup()
