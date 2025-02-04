import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, PhotoSize

from filters.general import EmailFilter
from keyboards.inline.base import create_inline_kb
from routers.companies.default import companies_command
from services.clients import get_client_service
from services.companies import get_company_service
from schemas.companies import CompanyCreateSchema
from schemas.representations import ClientReprSchema
from states.general import FSMCompanyCreate, FSMDefault, FSMCompanyRepr


logger = logging.getLogger(__name__)

router = Router()


@router.message(
    StateFilter(FSMCompanyCreate.fill_name),
    F.text.len() <= 50
)
async def name_done(
    message: Message, state: FSMContext, i18n: dict,
    client_data: ClientReprSchema
):
    logger.info('name_done')
    await state.update_data(
        new_company={
            'name': message.text,
            'creator_uuid': client_data.uuid
        }
    )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1
    )
    await message.answer(
        text=i18n['phrases']['company_create_fill_description'],
        reply_markup=keyboard
    )
    await state.set_state(FSMCompanyCreate.fill_description)


@router.message(
    StateFilter(FSMCompanyCreate.fill_name)
)
async def name_error(
    message: Message, i18n: dict
):
    logger.info('name_error')

    keyboard = await create_inline_kb(
        i18n['buttons'], 1
    )
    await message.answer(
        text=i18n['phrases']['company_create_fill_name_error'],
        reply_markup=keyboard
    )


@router.message(
    StateFilter(FSMCompanyCreate.fill_description),
    F.text.len() <= 300
)
async def description_done(
    message: Message, state: FSMContext, i18n: dict
):
    logger.info('description_done')

    data = await state.get_data()
    new_company = data['new_company']
    new_company['description'] = message.text
    await state.update_data(new_company=new_company)

    keyboard = await create_inline_kb(
        i18n['buttons'], 1
    )
    await message.answer(
        text=i18n['phrases']['company_create_fill_email'],
        reply_markup=keyboard
    )
    await state.set_state(FSMCompanyCreate.fill_email)


@router.message(
    StateFilter(FSMCompanyCreate.fill_description)
)
async def description_error(
    message: Message, i18n: dict
):
    logger.info('description_error')

    keyboard = await create_inline_kb(
        i18n['buttons'], 1
    )
    await message.answer(
        text=i18n['phrases']['company_create_fill_description_error'],
        reply_markup=keyboard
    )



@router.message(
    StateFilter(FSMCompanyCreate.fill_email),
    EmailFilter()
)
async def email_done(
    message: Message, state: FSMContext, i18n: dict
):
    logger.info('email_done')

    data = await state.get_data()
    new_company = data['new_company']
    new_company['email'] = message.text
    await state.update_data(new_company=new_company)

    buttons_list = ('fill_cancel_photo', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list
    )

    await message.answer(
        text=i18n['phrases']['company_create_upload_photo'],
        reply_markup=keyboard
    )
    await state.set_state(FSMCompanyCreate.upload_photo)


@router.message(
    StateFilter(FSMCompanyCreate.fill_email)
)
async def email_error(
    message: Message, i18n: dict
):
    logger.info('email_error')

    keyboard = await create_inline_kb(
        i18n['buttons'], 1
    )
    await message.answer(
        text=i18n['phrases']['company_create_fill_email_error'],
        reply_markup=keyboard
    )


@router.message(
    StateFilter(FSMCompanyCreate.upload_photo),
    F.photo[-1].as_('largest_photo')
)
async def photo_done(
    message: Message, state: FSMContext, i18n: dict,
    largest_photo: PhotoSize
):
    logger.info('photo_done')

    data = await state.get_data()
    new_company = data['new_company']
    new_company['photo_unique_id'] = largest_photo.file_unique_id
    new_company['photo_id'] = largest_photo.file_id
    await state.update_data(new_company=new_company)

    buttons_list = ('fill_cancel_video', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list
    )

    await message.answer(
        text=i18n['phrases']['company_create_upload_video'],
        reply_markup=keyboard
    )
    await state.set_state(FSMCompanyCreate.upload_video)


@router.callback_query(
    StateFilter(FSMCompanyCreate.upload_photo),
    F.data == 'fill_cancel_photo'
)
async def photo_cancel(
    callback: CallbackQuery, state: FSMContext, i18n: dict, bot: Bot
):
    logger.info('photo_cancel')

    buttons_list = ('fill_cancel_video', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list
    )

    await callback.message.edit_text(
        text=i18n['phrases']['company_create_upload_video'],
        reply_markup=keyboard
    )
    await state.set_state(FSMCompanyCreate.upload_video)


@router.message(
    StateFilter(FSMCompanyCreate.upload_photo)
)
async def photo_error(
    message: Message, i18n: dict
):
    logger.info('photo_error')

    buttons_list = ('fill_cancel_photo', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list
    )

    await message.answer(
        text=i18n['phrases']['company_create_upload_photo_error'],
        reply_markup=keyboard
    )


@router.message(
    StateFilter(FSMCompanyCreate.upload_video),
    F.video
)
async def video_done(
    message: Message, state: FSMContext, i18n: dict,
    client_data: ClientReprSchema
):
    logger.info('video_done')

    data = await state.get_data()
    new_company = data['new_company']
    new_company['video_unique_id'] = message.video.file_unique_id
    new_company['video_id'] = message.video.file_id
    await state.update_data(new_company=new_company)

    logger.info(f'video_done {new_company=}')

    company = CompanyCreateSchema(**new_company)
    service = get_company_service()
    result = await service.create(company)

    if result:
        client_service = get_client_service()
        await client_service.del_client_cache(client_data.tg_id)
        client_data = await client_service.get(client_data.tg_id)

    logger.info(f'video_done {result=}')

    await message.answer(
        text=i18n['phrases']['company_create_done']
    )
    await state.clear()
    await state.set_state(FSMCompanyRepr.repr)
    await companies_command(message, i18n, client_data, state)


@router.callback_query(
    StateFilter(FSMCompanyCreate.upload_video),
    F.data == 'fill_cancel_video'
)
async def video_cancel(
    callback: CallbackQuery, state: FSMContext, i18n: dict,
    client_data: ClientReprSchema
):
    logger.info('video_cancel')

    data = await state.get_data()
    new_company = data['new_company']
    await state.update_data(new_company=new_company)

    logger.info(f'video_done {new_company=}')

    company = CompanyCreateSchema(**new_company)
    service = get_company_service()
    result = await service.create(company)

    if result:
        client_service = get_client_service()
        await client_service.del_client_cache(client_data.tg_id)
        client_data = await client_service.get(client_data.tg_id)

    logger.info(f'video_done {result=}')

    await callback.message.answer(
        text=i18n['phrases']['company_create_done']
    )
    await state.clear()
    await state.set_state(FSMCompanyRepr.repr)
    await companies_command(callback.message, i18n, client_data, state)


@router.message(
    StateFilter(FSMCompanyCreate.upload_video)
)
async def video_error(
    message: Message, i18n: dict
):
    logger.info('video_error')

    buttons_list = ('fill_cancel_video', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list
    )

    await message.answer(
        text=i18n['phrases']['company_create_upload_video_error'],
        reply_markup=keyboard
    )
