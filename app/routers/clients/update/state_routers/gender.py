import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline.base import create_inline_kb
from routers.clients.update.state import FSMClientUpdate


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMClientUpdate.gender


@router.callback_query(
    StateFilter(router_state),
    F.data.in_(('gender_m', 'gender_f'))
)
async def gender_done(
    callback: CallbackQuery, state: FSMContext, i18n: dict
):
    await state.update_data(sex=callback.data[-1])

    data = await state.get_data()
    logger.info(f'gender_done {data=}')

    buttons_list = ('fill_cancel_photo', 'miss', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list
    )

    await callback.message.edit_text(
        text=i18n['phrases']['client_update_upload_photo'],
        reply_markup=keyboard
    )
    await state.set_state(FSMClientUpdate.photo)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'miss'
)
async def gender_miss(
    callback: CallbackQuery, state: FSMContext, i18n: dict
):
    buttons_list = ('fill_cancel_photo', 'miss', )
    keyboard = await create_inline_kb(
        i18n['buttons'],
        1,
        *buttons_list
    )

    await callback.message.answer(
        text=i18n['phrases']['client_update_upload_photo'],
        reply_markup=keyboard
    )
    await state.set_state(FSMClientUpdate.photo)


@router.message(
    StateFilter(router_state)
)
async def gender_error(
    message: Message, i18n: dict
):
    buttons_list = ('gender_m', 'gender_f', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 2,
        *buttons_list
    )
    await message.answer(
        text=i18n['phrases']['client_update_fill_gender_error'],
        reply_markup=keyboard
    )
