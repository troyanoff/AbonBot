import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, PhotoSize

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from services.clients import get_client_service
from services.companies import get_company_service
from schemas.companies import CompanyCreateSchema
from schemas.representations import ClientReprSchema
from routers.companies.create.state import FSMCompanyCreate
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMCompanyCreate.name


async def start_create(
    message: Message, state: FSMContext, lang: str,
    client_data: ClientReprSchema
):
    state_handler = f'{router_state.state}:start_create'
    logger.info(state_handler)

    await state.update_data(
        new_company={
            'creator_uuid': client_data.uuid
        }
    )

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *FSMCompanyCreate.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.start_create,
        reply_markup=keyboard
    )
    await state.set_state(FSMCompanyCreate.name)


@router.message(
    StateFilter(router_state),
    F.text.len() <= st.short_field_len
)
async def done(
    message: Message, state: FSMContext, lang: str,
    client_data: ClientReprSchema
):
    state_handler = f'{router_state.state}:done'
    logger.info(state_handler)

    data = await state.get_data()
    new_company_dict = data['new_company']
    new_company_dict['name'] = message.text
    await state.update_data(
        new_company=new_company_dict
    )

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *FSMCompanyCreate.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.done,
        reply_markup=keyboard
    )
    await state.set_state(FSMCompanyCreate.description)


@router.message(
    StateFilter(router_state)
)
async def error(
    message: Message, lang: str
):
    state_handler = f'{router_state.state}:error'
    logger.info(state_handler)

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *FSMCompanyCreate.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.error,
        reply_markup=keyboard
    )
