import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline.base import create_inline_kb
from routers.clients.update.state import FSMClientUpdate


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMClientUpdate.first_name


@router.message(
    StateFilter(router_state),
    F.text.isalpha()
)
async def first_name_done(
    message: Message, state: FSMContext, i18n: dict
):
    await state.update_data(first_name=message.text)

    buttons_list = ('miss', )
    keyboard = await create_inline_kb(
        i18n['buttons'],
        1,
        *buttons_list
    )

    await message.answer(
        text=i18n['phrases']['client_update_fill_last_name'],
        reply_markup=keyboard
    )
    await state.set_state(FSMClientUpdate.last_name)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'miss'
)
async def first_name_miss(
    callback: CallbackQuery, state: FSMContext, i18n: dict
):
    buttons_list = ('miss', )
    keyboard = await create_inline_kb(
        i18n['buttons'],
        1,
        *buttons_list
    )

    await callback.message.answer(
        text=i18n['phrases']['client_update_fill_last_name'],
        reply_markup=keyboard
    )
    await state.set_state(FSMClientUpdate.last_name)


@router.message(
    StateFilter(router_state)
)
async def first_name_error(
    message: Message, i18n: dict
):
    buttons_list = ('miss', )
    keyboard = await create_inline_kb(
        i18n['buttons'],
        1,
        *buttons_list,
        cancel_button=False,
    )

    await message.answer(
        text=i18n['phrases']['client_update_fill_first_name_error'],
        reply_markup=keyboard
    )
