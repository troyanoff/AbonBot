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
from keyboards.inline.base import (
    create_simply_inline_kb, create_offset_inline_kb
)
from keyboards.inline.companies import company_repr_inline
from routers.companies.manage.state_routers.default.handlers import manage
from services.companies import get_company_service
from routers.companies.representation.state import FSMCompanyRepr
from routers.default.state import FSMDefault
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
            message=message, lang=lang, state=state,
            company=companies.items[0]
        )
        return

    companies_offset = []
    count = 1
    for company in companies.items:
        companies_offset.append(
            {
                'uuid': company.uuid,
                'name': company.name,
                'num': count
            }
        )
        count += 1

    await state.update_data(
        companies_offset=companies_offset
    )

    keyboard = await create_offset_inline_kb(
        data=companies_offset,
        callback_prefix='company',
        side_index=0,
        back=False,
        lang=lang
    )
    await message.answer(
        text=terminology_lang.terms.company_list,
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(router_state),
    F.data.regexp((r'^back:\d+$'))
)
async def back(
    callback: CallbackQuery,
    state: FSMContext,
    client_data: ClientReprSchema,
    lang: str
):
    state_handler = f'{router_state.state}:back'
    logger.info(state_handler)

    service = get_company_service()
    companies: CompanyListSchema = await service.get_list(
        client_data.uuid.__str__())

    if await st.is_debag():
        logger.info(f'{companies=}')

    if isinstance(companies, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await callback.message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    terminology_lang: Lang = getattr(terminology, lang)

    data = await state.get_data()
    companies_offset = data['companies_offset']
    side_index = int(callback.data.split(':')[-1])

    keyboard = await create_offset_inline_kb(
        data=companies_offset,
        callback_prefix='company',
        side_index=side_index,
        back=True,
        lang=lang
    )

    await callback.message.edit_text(
        text=terminology_lang.terms.company_list,
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(router_state),
    F.data.regexp((r'^forward:\d+$'))
)
async def forward(
    callback: CallbackQuery,
    state: FSMContext,
    client_data: ClientReprSchema,
    lang: str
):
    state_handler = f'{router_state.state}:forward'
    logger.info(state_handler)

    service = get_company_service()
    companies: CompanyListSchema = await service.get_list(
        client_data.uuid.__str__())

    if await st.is_debag():
        logger.info(f'{companies=}')

    if isinstance(companies, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await callback.message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    terminology_lang: Lang = getattr(terminology, lang)

    data = await state.get_data()
    companies_offset = data['companies_offset']
    side_index = int(callback.data.split(':')[-1])

    keyboard = await create_offset_inline_kb(
        data=companies_offset,
        callback_prefix='company',
        side_index=side_index,
        back=False,
        lang=lang
    )

    await callback.message.edit_text(
        text=terminology_lang.terms.company_list,
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(router_state),
    F.data.regexp((
        r'^company:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-'
        r'[0-9a-f]{12}$'
    ))
)
async def to_manage(
    callback: CallbackQuery,
    state: FSMContext,
    client_data: ClientReprSchema,
    lang: str
):
    state_handler = f'{router_state.state}:to_manage'
    logger.info(state_handler)

    company_uuid = callback.data.split(':')[-1]
    service = get_company_service()
    company: CompanyListSchema = await service.get(
        uuid=company_uuid)

    if isinstance(company, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await callback.message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    await manage(
        message=callback.message, lang=lang,
        state=state, company=company, edit_text=True
    )
