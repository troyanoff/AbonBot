import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, PhotoSize

from keyboards.inline.base import create_inline_kb
from keyboards.menu.base import set_client_menu
from services.clients import get_client_service
from schemas.clients import ClientCreateSchema
from states.general import FSMClientCreate, FSMDefault


logger = logging.getLogger(__name__)

router = Router()


@router.message(
    StateFilter(FSMClientCreate.fill_first_name),
    F.text.isalpha()
)
async def first_name_done(
    message: Message, state: FSMContext, i18n: dict
):
    logger.info('first_name_done')
    await state.update_data(first_name=message.text)
    await message.answer(
        text=i18n['phrases']['client_create_fill_last_name']
    )
    await state.set_state(FSMClientCreate.fill_last_name)


@router.message(
    StateFilter(FSMClientCreate.fill_first_name)
)
async def first_name_error(
    message: Message, i18n: dict
):
    await message.answer(
        text=i18n['phrases']['client_create_fill_first_name_error']
    )


@router.message(
    StateFilter(FSMClientCreate.fill_last_name),
    F.text.isalpha()
)
async def last_name_done(
    message: Message, state: FSMContext, i18n: dict
):
    logger.info('last_name_done')

    await state.update_data(last_name=message.text)

    data = await state.get_data()
    logger.info(f'last_name_done {data=}')

    buttons_list = ('gender_m', 'gender_f', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 2,
        *buttons_list,
        cancel_button=False
    )
    await message.answer(
        text=i18n['phrases']['client_create_fill_gender'],
        reply_markup=keyboard
    )
    await state.set_state(FSMClientCreate.fill_gender)


@router.message(
    StateFilter(FSMClientCreate.fill_last_name)
)
async def last_name_error(
    message: Message, i18n: dict
):
    await message.answer(
        text=i18n['phrases']['client_create_fill_last_name_error']
    )


@router.callback_query(
    StateFilter(FSMClientCreate.fill_gender),
    F.data.in_(('gender_m', 'gender_f'))
)
async def gender_done(
    callback: CallbackQuery, state: FSMContext, i18n: dict
):
    
    await state.update_data(sex=callback.data[-1])

    data = await state.get_data()
    logger.info(f'gender_done {data=}')

    buttons_list = ('fill_cancel_photo', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list,
        cancel_button=False
    )

    await callback.message.edit_text(
        text=i18n['phrases']['client_create_upload_photo'],
        reply_markup=keyboard
    )
    await state.set_state(FSMClientCreate.upload_photo)


@router.message(
    StateFilter(FSMClientCreate.fill_gender)
)
async def gender_error(
    message: Message, i18n: dict
):
    
    buttons_list = ('gender_m', 'gender_f', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 2,
        *buttons_list,
        cancel_button=False
    )
    await message.answer(
        text=i18n['phrases']['client_create_fill_gender_error'],
        reply_markup=keyboard
    )


@router.message(
    StateFilter(FSMClientCreate.upload_photo),
    F.photo[-1].as_('largest_photo')
)
async def photo_done(
    message: Message, state: FSMContext, i18n: dict,
    largest_photo: PhotoSize, bot: Bot
):
    
    await state.update_data(
        tg_id=message.from_user.id,
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )

    data = await state.get_data()
    logger.info(f'photo_done {data=}')
    client_data = ClientCreateSchema(**data)

    service = get_client_service()

    await service.create(client_data)

    await set_client_menu(bot, client_data.tg_id, i18n['menu'])

    await message.answer(
        text=i18n['phrases']['client_create_done'],
        reply_markup=None
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.callback_query(
    StateFilter(FSMClientCreate.upload_photo),
    F.data == 'fill_cancel_photo'
)
async def photo_cancel(
    callback: CallbackQuery, state: FSMContext, i18n: dict, bot: Bot
):
    
    await state.update_data(
        tg_id=callback.from_user.id,
    )

    data = await state.get_data()
    client_data = ClientCreateSchema(**data)

    service = get_client_service()

    await service.create(client_data)

    await set_client_menu(bot, client_data.tg_id, i18n['menu'])

    await callback.message.edit_text(
        text=i18n['phrases']['client_create_done'],
        reply_markup=None
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.message(
    StateFilter(FSMClientCreate.fill_gender)
)
async def photo_error(
    message: Message, i18n: dict
):
    
    buttons_list = ('fill_cancel_photo', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list,
        cancel_button=False
    )

    await message.answer(
        text=i18n['phrases']['client_create_upload_photo_error'],
        reply_markup=keyboard
    )
