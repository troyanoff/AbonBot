
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.start import FSMStart

from phrases.ru import phrases
from schemas.representations import ClientReprSchema


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
