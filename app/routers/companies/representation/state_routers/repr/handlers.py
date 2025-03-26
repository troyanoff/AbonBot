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

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from keyboards.inline.companies import company_repr_inline
from routers.companies.manage.state_routers.default.handlers import manage
from services.companies import get_company_service
from routers.companies.representation.state import FSMCompanyRepr
from schemas.utils import FailSchema
from schemas.representations import ClientReprSchema, CompanyListSchema
from utils.support import choice_back_company, choice_forward_company
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMCompanyRepr.repr


async def companies_repr(
    message: Message,
    lang: str,
    client_data: ClientReprSchema,
    state: FSMContext,
):
    state_handler = f'{router_state.state}:companies_repr'
    logger.info(state_handler)

    service = get_company_service()
    companies: CompanyListSchema = await service.get_list(
        client_data.uuid.__str__())

    if await st.is_debag():
        logger.info(f'{companies=}')

    core_term_lang: core_Lang = getattr(core_term, lang)
    if isinstance(companies, FailSchema):
        await message.answer(
            text=core_term_lang.terms.error
        )
        return

    terminology_lang: Lang = getattr(terminology, lang)
    if not companies.total_count:
        core_buttons = await core_term_lang.buttons.get_dict_with(
            *FSMCompanyRepr.core_buttons)

        keyboard = await create_simply_inline_kb(
            core_buttons,
            1
        )
        await message.answer(
            text=terminology_lang.terms.not_company,
            reply_markup=keyboard
        )
        return

    if companies.total_count == 1:
        await manage(
            message=message, lang=lang, client_data=client_data, state=state,
            company=companies.items[0]
        )
        return




    # if not client_data.companies_count:
    #     await message.answer(
    #         text=i18n['phrases']['company_empty']
    #     )
    #     return


    # service = get_company_service()
    # companies = await service.get_list(client_data.uuid)

    # keyboard = await company_repr_inline(i18n, len(companies) == 1)

    # company = companies[0]

    # await state.update_data(now_company_uuid=company.uuid)

    # text = i18n['phrases']['company_repr'].format(
    #     number=1,
    #     name=company.name,
    #     description=company.description
    # )

    # await message.answer(
    #     text=text,
    #     reply_markup=keyboard
    # )


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
    StateFilter(router_state),
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
    StateFilter(router_state),
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
