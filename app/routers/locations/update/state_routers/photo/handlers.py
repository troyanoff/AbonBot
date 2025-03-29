import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PhotoSize

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from routers.locations.update.state import package_state
from ..description.terminology import (
    terminology as last_term, Lang as last_Lang
)
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = package_state.photo
next_state = package_state.city


@router.message(
    StateFilter(router_state),
    F.photo[-1].as_('largest_photo')
)
async def done(
    message: Message, state: FSMContext, lang: str,
    largest_photo: PhotoSize
):
    state_handler = f'{router_state.state}:done'
    logger.info(state_handler)

    data = await state.get_data()

    update_location_dict = data['update_location']
    update_location_dict['photo_unique_id'] = largest_photo.file_unique_id
    update_location_dict['photo_id'] = largest_photo.file_id
    await state.update_data(
        update_location=update_location_dict
    )

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


@router.callback_query(
    StateFilter(router_state),
    F.data.in_(package_state.photo_callbacks)
)
async def cancel(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:cancel'
    logger.info(state_handler)

    data = await state.get_data()

    update_location_dict = data['update_location']
    update_location_dict['photo_unique_id'] = ''
    update_location_dict['photo_id'] = ''
    await state.update_data(
        update_location=update_location_dict
    )

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
    await callback.message.answer(
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
    logger.info(state_handler)

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)
    last_term_lang: last_Lang = getattr(last_term, lang)

    buttons = last_term_lang.buttons.__dict__
    core_buttons = await core_term_lang.buttons.get_dict_with(
        *package_state.core_buttons)
    buttons.update(core_buttons)

    keyboard = await create_simply_inline_kb(
        buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.error,
        reply_markup=keyboard
    )
