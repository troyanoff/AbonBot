import logging

from aiogram import Router, F
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
from keyboards.inline.factories import company_inline, CompanyFactory
from services.companies import get_company_service
from states.general import FSMDefault, FSMCompanyRepr, FSMCompanyCreate
from schemas.representations import ClientReprSchema


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

    client_companies = [i.model_dump_json() for i in companies]
    await state.set_data({'client_companies': client_companies})


    kb_builder = InlineKeyboardBuilder()
    kb_buttons: list[InlineKeyboardButton] = []
    kb_buttons.append(
        InlineKeyboardButton(
            text=i18n['buttons']['back'],
            callback_data='back'
        )
    )
    kb_buttons.append(
        InlineKeyboardButton(
            text=i18n['buttons']['forward'],
            callback_data='forward'
        )
    )
    kb_builder.row(*kb_buttons, width=2)
    kb_builder.row(InlineKeyboardButton(
        text=i18n['buttons']['manage_company'],
        callback_data='manage_company'
    ))
    kb_builder.row(InlineKeyboardButton(
        text=i18n['buttons']['create_company'],
        callback_data='create_company'
    ))
    kb_builder.row(InlineKeyboardButton(
        text=i18n['buttons']['cancel'],
        callback_data='cancel'
    ))
    keyboard = kb_builder.as_markup()

    company = companies[0]

    text = i18n['phrases']['company_header']
    text += i18n['phrases']['company_repr'].format(
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
