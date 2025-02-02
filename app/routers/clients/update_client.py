import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, PhotoSize

from keyboards.inline.base import create_inline_kb
from services.clients import get_client_service
from schemas.representations import ClientReprSchema
from states.general import FSMClientUpdate, FSMDefault


logger = logging.getLogger(__name__)

router = Router()


@router.message(
    StateFilter(FSMClientUpdate.fill_first_name),
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
    await state.set_state(FSMClientUpdate.fill_last_name)


@router.callback_query(
    StateFilter(FSMClientUpdate.fill_first_name),
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
    await state.set_state(FSMClientUpdate.fill_last_name)


@router.message(
    StateFilter(FSMClientUpdate.fill_first_name)
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


@router.message(
    StateFilter(FSMClientUpdate.fill_last_name),
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
    await state.set_state(FSMClientUpdate.fill_gender)


@router.callback_query(
    StateFilter(FSMClientUpdate.fill_last_name),
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
    await state.set_state(FSMClientUpdate.fill_gender)


@router.message(
    StateFilter(FSMClientUpdate.fill_last_name)
)
async def last_name_error(
    message: Message, i18n: dict
):
    
    buttons_list = ('cancel', )
    keyboard = await create_inline_kb(
        i18n['buttons'],
        1,
        *buttons_list,
        cancel_button=False,
    )

    await message.answer(
        text=i18n['phrases']['client_update_fill_last_name_error']
    )


@router.callback_query(
    StateFilter(FSMClientUpdate.fill_gender),
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
    await state.set_state(FSMClientUpdate.upload_photo)


@router.callback_query(
    StateFilter(FSMClientUpdate.fill_gender),
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
    await state.set_state(FSMClientUpdate.upload_photo)


@router.message(
    StateFilter(FSMClientUpdate.fill_gender)
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


@router.message(
    StateFilter(FSMClientUpdate.upload_photo),
    F.photo[-1].as_('largest_photo')
)
async def photo_done(
    message: Message, state: FSMContext, i18n: dict,
    largest_photo: PhotoSize, bot: Bot,
    client_data: ClientReprSchema
):
    
    await state.update_data(
        uuid=client_data.uuid,
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )

    data = await state.get_data()
    logger.info(f'photo_done {data=}')
    service = get_client_service()
    await service.update(data)

    await message.answer(
        text=i18n['phrases']['client_update_done']
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.callback_query(
    StateFilter(FSMClientUpdate.upload_photo),
    F.data == 'miss'
)
async def gender_miss(
    callback: CallbackQuery, state: FSMContext, i18n: dict,
    client_data: ClientReprSchema
):
    await state.update_data(
        uuid=client_data.uuid
    )

    data = await state.get_data()
    logger.info(f'photo_done {data=}')
    service = get_client_service()
    await service.update(data)

    await callback.message.edit_text(
        text=i18n['phrases']['client_update_done']
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.callback_query(
    StateFilter(FSMClientUpdate.upload_photo),
    F.data == 'fill_cancel_photo'
)
async def photo_cancel(
    callback: CallbackQuery, state: FSMContext, i18n: dict, bot: Bot,
    client_data: ClientReprSchema
):
    await state.update_data(
        uuid=client_data.uuid,
        photo_unique_id=None,
        photo_id=None
    )

    data = await state.get_data()
    logger.info(f'photo_done {data=}')
    service = get_client_service()
    await service.update(data)

    await callback.message.edit_text(
        text=i18n['phrases']['client_update_done']
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.message(
    StateFilter(FSMClientUpdate.upload_photo)
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
