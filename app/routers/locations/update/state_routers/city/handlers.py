import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from routers.locations.update.state import package_state
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = package_state.city
next_state = package_state.street


@router.message(
    StateFilter(router_state),
    F.text.len() <= st.short_field_len
)
async def done(
    message: Message, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:done'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    data = await state.get_data()
    update_location_dict = data['update_location']
    update_location_dict['city'] = message.text
    await state.update_data(
        update_location=update_location_dict
    )

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *package_state.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.done,
        reply_markup=keyboard
    )
    await state.set_state(next_state)


@router.callback_query(
    StateFilter(router_state),
    F.data == package_state.miss_button
)
async def miss_state(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:miss_state'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)
    buttons = await core_term_lang.buttons.get_dict_with(
        *package_state.core_buttons)
    keyboard = await create_simply_inline_kb(
        buttons,
        1
    )

    await callback.message.edit_text(
        text=terminology_lang.terms.done,
        reply_markup=keyboard
    )
    await state.set_state(next_state)


@router.message(
    StateFilter(router_state)
)
async def error(
    message: Message, lang: str
):
    state_handler = f'{router_state.state}:error'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *package_state.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.error,
        reply_markup=keyboard
    )
