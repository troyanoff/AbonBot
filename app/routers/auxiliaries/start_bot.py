
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.general import FSMClientCreate, FSMStart


router = Router()


@router.message(Command(commands='registration'), StateFilter(FSMStart.start))
async def process_cancel_command(
    message: Message,
    state: FSMContext,
    i18n: dict
):
    await message.answer(
        text=i18n['phrases']['client_create_fill_first_name']
    )

    await state.set_state(FSMClientCreate.fill_first_name)
