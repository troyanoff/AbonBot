import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.config import settings as st
from keyboards.inline.base import create_simply_inline_kb
from routers.clients.create.state import FSMClientCreate
from .terminology import terminology, Lang
from ..last_name.terminology import terminology as last_term, Lang as last_Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMClientCreate.gender


@router.callback_query(
    StateFilter(router_state),
    F.data.in_(FSMClientCreate.gender_callbacks)
)
async def gender_done(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:done'
    logger.info(state_handler)

    await state.update_data(sex=callback.data[-1])

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    terminology_lang: Lang = getattr(terminology, lang)
    keyboard = await create_simply_inline_kb(
        buttons=terminology_lang.buttons.__dict__,
        width=1
    )

    await callback.message.edit_text(
        text=terminology_lang.terms.done,
        reply_markup=keyboard
    )
    await state.set_state(FSMClientCreate.photo)


@router.message(
    StateFilter(router_state)
)
async def gender_error(
    message: Message, lang: str
):
    state_handler = f'{router_state.state}:error'
    logger.info(state_handler)

    last_term_lang: last_Lang = getattr(last_term, lang)
    keyboard = await create_simply_inline_kb(
        buttons=last_term_lang.buttons.__dict__,
        width=1
    )

    terminology_lang: Lang = getattr(terminology, lang)
    await message.answer(
        text=terminology_lang.terms.error,
        reply_markup=keyboard
    )
