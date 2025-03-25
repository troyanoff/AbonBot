import logging

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PhotoSize

from keyboards.inline.base import create_inline_kb
from services.clients import get_client_service
from schemas.representations import ClientReprSchema
from routers.clients.update.state import FSMClientUpdate
from routers.default.state import FSMDefault


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMClientUpdate.photo


@router.message(
    StateFilter(router_state),
    F.photo[-1].as_('largest_photo')
)
async def photo_done(
    message: Message, state: FSMContext, i18n: dict,
    largest_photo: PhotoSize, bot: Bot,
    client_data: ClientReprSchema
):
    await state.update_data(
        uuid=client_data.uuid.__str__(),
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )

    data = await state.get_data()
    logger.info(f'photo_done {data=}')
    service = get_client_service()
    result = await service.update(message.from_user.id, data)
    if not result:
        await message.answer(
            text=i18n['phrases']['error_phrase']
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    await message.answer(
        text=i18n['phrases']['client_update_done']
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'miss'
)
async def photo_miss(
    callback: CallbackQuery, state: FSMContext, i18n: dict,
    client_data: ClientReprSchema
):
    await state.update_data(
        uuid=client_data.uuid.__str__()
    )

    data = await state.get_data()
    logger.info(f'photo_done {data=}')
    service = get_client_service()
    result = await service.update(callback.from_user.id, data)
    if not result:
        await callback.message.edit_text(
            text=i18n['phrases']['error_phrase'],
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    await callback.message.edit_text(
        text=i18n['phrases']['client_update_done']
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'fill_cancel_photo'
)
async def photo_cancel(
    callback: CallbackQuery, state: FSMContext, i18n: dict, bot: Bot,
    client_data: ClientReprSchema
):
    await state.update_data(
        uuid=client_data.uuid.__str__(),
        photo_unique_id='',
        photo_id=''
    )

    data = await state.get_data()
    logger.info(f'photo_done {data=}')
    service = get_client_service()
    result = await service.update(callback.from_user.id, data)
    if not result:
        await callback.message.edit_text(
            text=i18n['phrases']['error_phrase'],
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    await callback.message.edit_text(
        text=i18n['phrases']['client_update_done']
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.message(
    StateFilter(router_state)
)
async def photo_error(
    message: Message, i18n: dict
):
    buttons_list = ('miss', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list
    )

    await message.answer(
        text=i18n['phrases']['client_update_upload_photo_error'],
        reply_markup=keyboard
    )
