import logging

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from routers.clients.create.queue import handler
from routers.auxiliaries.start.state import FSMStart
from handlers.base import create_request_tg, RequestTG


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMStart.start


@router.message(Command(commands='registration'), StateFilter(router_state))
async def registration(
    message: Message,
    state: FSMContext,
    lang: str
):
    request_tg: RequestTG = await create_request_tg(
        'registration',
        update=message,
        lang=lang,
        state=state,
        logger=logger
    )
    await handler(request_tg)
