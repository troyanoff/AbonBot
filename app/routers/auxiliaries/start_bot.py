
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards.inline.base import create_inline_kb
from states.create_client import FSMClietnCreate
from schemas.representations import ClientReprSchema


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(
    message: Message, i18n: dict, client_data: ClientReprSchema | None
):
    # await message.answer(text='sd', reply_markup=ReplyKeyboardRemove())
    if not client_data:
        await message.answer(
            text=i18n['phrases']['start_unknow']
        )
        return

    await message.answer(
        text=i18n['phrases']['start']
    )


@router.message(Command(commands='registration'), StateFilter(default_state))
async def process_cancel_command(
    message: Message,
    state: FSMContext,
    i18n: dict,
    client_data: ClientReprSchema | None
):
    if client_data:
        return
    await message.answer(
        text=i18n['phrases']['client_create_fill_first_name']
    )
    
    await state.set_state(FSMClietnCreate.fill_first_name)
