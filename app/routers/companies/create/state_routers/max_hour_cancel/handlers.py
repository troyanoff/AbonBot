import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from services.companies import get_company_service
from schemas.companies import CompanyCreateSchema
from schemas.utils import FailSchema
from routers.companies.create.state import FSMCompanyCreate
from routers.default.state import FSMDefault
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMCompanyCreate.max_hour_cancel


@router.message(
    StateFilter(router_state),
    F.text.regexp(r'^\d+$')
)
async def done(
    message: Message, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:done'
    logger.info(state_handler)

    data = await state.get_data()
    new_company_dict = data['new_company']
    new_company_dict['max_hour_cancel'] = int(message.text)
    await state.update_data(
        new_company=new_company_dict
    )

    data = await state.get_data()
    if await st.is_debag():
        logger.info(f'{state_handler} {data=}')

    service = get_company_service()
    result = await service.create(CompanyCreateSchema(**data['new_company']))

    if isinstance(result, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    terminology_lang: Lang = getattr(terminology, lang)

    await message.answer(
        text=terminology_lang.terms.done
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


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
