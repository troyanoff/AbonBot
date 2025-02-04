import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from time import time

from core.config import settings
from keyboards.inline.base import create_inline_kb
from keyboards.inline.companies import company_repr_inline
from services.companies import get_company_service
from states.general import (
    FSMDefault, FSMCompanyRepr, FSMCompanyCreate, FSMCompanyManage
)
from schemas.representations import ClientReprSchema
from utils.support import choice_back_company, choice_forward_company


logger = logging.getLogger(__name__)

router = Router()


@router.message(Command(commands='companies'), StateFilter(FSMDefault.default))
async def companies_command(
    message: Message,
    i18n: dict,
    client_data: ClientReprSchema,
    state: FSMContext,
):
    if not client_data.companies_count:
        await message.answer(
            text=i18n['phrases']['company_empty']
        )
        return

    await state.set_state(FSMCompanyRepr.repr)

    service = get_company_service()
    companies = await service.get_list(client_data.uuid)

    keyboard = await company_repr_inline(i18n, len(companies) == 1)

    company = companies[0]

    await state.update_data(now_company_uuid=company.uuid)

    text = i18n['phrases']['company_repr'].format(
        number=1,
        name=company.name,
        description=company.description
    )

    await message.answer(
        text=text,
        reply_markup=keyboard
    )


# @router.callback_query(
#     # CompanyFactory.filter(),
#     StateFilter(FSMCompanyRepr.repr)
# )
# async def company(
#     callback: CallbackQuery,
#     # callback_data: CompanyFactory,
#     i18n: dict,
#     state: FSMContext,
#     client_data: ClientReprSchema,
# ):
#     logger.info('company handler')
#     # text = callback_data

#     # company_uuid = callback_data.uuid
#     await callback.message.answer(text='company handler repr')


@router.callback_query(
    StateFilter(FSMCompanyRepr.repr),
    F.data == 'forward'
)
async def forward_company(
    callback: CallbackQuery,
    # callback_data: CompanyFactory,
    i18n: dict,
    state: FSMContext,
    client_data: ClientReprSchema,
):
    logger.info('forward_company handler')

    service = get_company_service()
    companies = await service.get_list(client_data.uuid)

    state_data = await state.get_data()

    company = await choice_forward_company(
        state_data['now_company_uuid'], companies)

    keyboard = await company_repr_inline(i18n, len(companies) == 1)

    await state.update_data(now_company_uuid=company.uuid)

    text = i18n['phrases']['company_repr'].format(
        number=1,
        name=company.name,
        description=company.description
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(FSMCompanyRepr.repr),
    F.data == 'back'
)
async def back_company(
    callback: CallbackQuery,
    # callback_data: CompanyFactory,
    i18n: dict,
    state: FSMContext,
    client_data: ClientReprSchema,
    bot: Bot
):
    logger.info('back_company handler')

    service = get_company_service()
    companies = await service.get_list(client_data.uuid)

    state_data = await state.get_data()

    company = await choice_back_company(
        state_data['now_company_uuid'], companies)

    keyboard = await company_repr_inline(i18n, len(companies) == 1)

    await state.update_data(now_company_uuid=company.uuid)

    text = i18n['phrases']['company_repr'].format(
        number=1,
        name=company.name,
        description=company.description
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(FSMCompanyRepr.repr),
    F.data == 'create_company'
)
async def create_company(
    callback: CallbackQuery,
    # callback_data: CompanyFactory,
    i18n: dict,
    state: FSMContext,
    client_data: ClientReprSchema,
):
    logger.info('create_company handler')
    await state.set_state(FSMCompanyCreate.fill_name)

    keyboard = await create_inline_kb(
        i18n['buttons'], 1
    )

    await callback.message.answer(
        text=i18n['phrases']['company_create_fill_name'],
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(FSMCompanyRepr.repr),
    F.data == 'manage_company'
)
async def manage_company(
    callback: CallbackQuery,
    # callback_data: CompanyFactory,
    i18n: dict,
    state: FSMContext,
    client_data: ClientReprSchema,
):
    logger.info('manage_company handler')
    await state.set_state(FSMCompanyManage.manage)

    data = await state.get_data()
    logger.info(f'{data=}')

    buttons = (
        'locations', 'trainings', 'instructors', 'abonnements',
        'timeslots'
    )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons
    )

    await callback.message.answer(
        text=i18n['phrases']['company_manage_default'],
        reply_markup=keyboard
    )
