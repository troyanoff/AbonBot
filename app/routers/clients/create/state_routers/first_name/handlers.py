import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from routers.clients.create.state import FSMClientCreate
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMClientCreate.first_name


@router.message(
    StateFilter(router_state),
    F.text.isalpha()
)
async def done(
    message: Message, state: FSMContext, lang: str
):
    logger.info(f'{router_state.state}:done')
    await state.update_data(first_name=message.text)

    terminology_lang: Lang = getattr(terminology, lang)
    await message.answer(
        text=terminology_lang.terms.done
    )
    await state.set_state(FSMClientCreate.last_name)


@router.message(
    StateFilter(router_state)
)
async def error(
    message: Message, lang: str
):
    logger.info(f'{router_state.state}:error')

    terminology_lang: Lang = getattr(terminology, lang)
    await message.answer(
        text=terminology_lang.terms.error
    )
