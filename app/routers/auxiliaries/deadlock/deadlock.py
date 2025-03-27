import logging

from aiogram import Router
from aiogram.types import Message, ErrorEvent, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.general import FSMStart

from core.terminology import terminology as core_term, Lang as core_Lang
from schemas.representations import ClientReprSchema


logger = logging.getLogger(__name__)

router = Router()


@router.message()
async def deadlock_msg(
    message: Message,
    lang: str,
    state: FSMContext,
    client_data: ClientReprSchema | None
):
    core_term_lang: core_Lang = getattr(core_term, lang)
    if not client_data:
        await message.answer(
            text=core_term_lang.terms.start_unknow
        )
        await state.set_state(FSMStart.start)
        return
    await message.answer(text=core_term_lang.terms.deadlock)


@router.callback_query()
async def deadlock_callback(
    callback: CallbackQuery,
    lang: str,
    state: FSMContext,
    client_data: ClientReprSchema | None
):
    core_term_lang: core_Lang = getattr(core_term, lang)
    if not client_data:
        await callback.message.answer(
            text=core_term_lang.terms.start_unknow
        )
        await state.set_state(FSMStart.start)
        return
    await callback.message.answer(text=core_term_lang.terms.deadlock)


@router.error()
async def error_handler(event: ErrorEvent):
    logger.critical(
        'Critical error caused by %s', event.exception, exc_info=True)
