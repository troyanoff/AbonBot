import asyncio
import logging

from aiogram import Router
from aiogram.types import Message, ErrorEvent, CallbackQuery
from aiogram.fsm.context import FSMContext

from core.terminology import terminology as core_term, Lang as core_Lang
from routers.default.state import FSMStart
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
    msg = await message.answer(text=core_term_lang.terms.deadlock)
    await asyncio.sleep(1.5)
    await msg.delete()


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
    msg = await callback.message.answer(text=core_term_lang.terms.deadlock)
    await asyncio.sleep(1.5)
    await msg.delete()


@router.error()
async def error_handler(event: ErrorEvent):
    logger.critical(
        'Critical error caused by %s', event.exception, exc_info=True)
