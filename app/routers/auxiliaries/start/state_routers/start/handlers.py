import logging

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from routers.clients.create.state import FSMClientCreate
from routers.auxiliaries.start.state import FSMStart
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMStart.start


@router.message(Command(commands='registration'), StateFilter(router_state))
async def registration(
    message: Message,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:registration'
    logger.info(state_handler)
    terminology_lang: Lang = getattr(terminology, lang)
    await message.answer(
        text=terminology_lang.terms.registration
    )

    await state.set_state(FSMClientCreate.first_name)
