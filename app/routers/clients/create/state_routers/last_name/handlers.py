import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config import settings as st
from keyboards.inline.base import create_simply_inline_kb
from routers.clients.create.state import FSMClientCreate
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMClientCreate.last_name


@router.message(
    StateFilter(router_state),
    F.text.isalpha()
)
async def done(
    message: Message, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:done'
    logger.info(state_handler)

    await state.update_data(last_name=message.text)

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    terminology_lang: Lang = getattr(terminology, lang)
    keyboard = await create_simply_inline_kb(
        terminology_lang.buttons.__dict__,
        2
    )
    await message.answer(
        text=terminology_lang.terms.done,
        reply_markup=keyboard
    )
    await state.set_state(FSMClientCreate.gender)


@router.message(
    StateFilter(router_state)
)
async def error(
    message: Message, lang: str
):
    state_handler = f'{router_state.state}:error'
    logger.info(state_handler)
    terminology_lang: Lang = getattr(terminology, lang)
    await message.answer(
        text=terminology_lang.terms.error
    )
