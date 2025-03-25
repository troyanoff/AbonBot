import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline.base import create_inline_kb
from routers.clients.update.state import FSMClientUpdate


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMClientUpdate.last_name


@router.message(
    StateFilter(router_state),
    F.text.isalpha()
)
async def last_name_done(
    message: Message, state: FSMContext, i18n: dict
):
    logger.info('last_name_done')

    await state.update_data(last_name=message.text)

    data = await state.get_data()
    logger.info(f'last_name_done {data=}')

    buttons_list = ('gender_m', 'gender_f', 'miss', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 2,
        *buttons_list
    )
    await message.answer(
        text=i18n['phrases']['client_update_fill_gender'],
        reply_markup=keyboard
    )
    await state.set_state(FSMClientUpdate.gender)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'miss'
)
async def last_name_miss(
    callback: CallbackQuery, state: FSMContext, i18n: dict
):
    buttons_list = ('gender_m', 'gender_f', 'miss', )
    keyboard = await create_inline_kb(
        i18n['buttons'],
        1,
        *buttons_list
    )

    await callback.message.answer(
        text=i18n['phrases']['client_update_fill_gender'],
        reply_markup=keyboard
    )
    await state.set_state(FSMClientUpdate.gender)


@router.message(
    StateFilter(router_state)
)
async def last_name_error(
    message: Message, i18n: dict
):
    await message.answer(
        text=i18n['phrases']['client_update_fill_last_name_error']
    )
