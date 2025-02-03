import logging

from aiogram import Router
from aiogram.types import Message, ErrorEvent
from aiogram.fsm.context import FSMContext
from states.general import FSMStart

from phrases.ru import phrases
from schemas.representations import ClientReprSchema


logger = logging.getLogger(__name__)

router = Router()

@router.message()
async def send_echo(
    message: Message,
    i18n: dict,
    state: FSMContext,
    client_data: ClientReprSchema | None
):
    if not client_data:
        await message.answer(
            text=i18n['phrases']['start_unknow']
        )
        await state.set_state(FSMStart.start)
        return
    await message.reply(text=i18n['phrases']['deadlock'])


@router.error()
async def error_handler(event: ErrorEvent):
    logger.critical(
        'Critical error caused by %s', event.exception, exc_info=True)
