
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from routers.clients.create.state import FSMClientCreate
from states.general import FSMStart


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

    await state.set_state(FSMClientCreate.first_name)
