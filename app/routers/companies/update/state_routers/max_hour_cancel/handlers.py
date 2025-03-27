import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from services.companies import get_company_service
from schemas.companies import CompanyUpdateSchema
from schemas.utils import FailSchema
from routers.companies.update.state import FSMCompanyUpdate
from routers.companies.manage.state_routers.default.handlers import manage
from routers.default.state import FSMDefault
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMCompanyUpdate.max_hour_cancel


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
    update_company_dict = data['update_company']
    update_company_dict['max_hour_cancel'] = int(message.text)
    await state.update_data(
        update_company=update_company_dict
    )

    data = await state.get_data()
    if await st.is_debag():
        logger.info(f'{state_handler} {data=}')

    service = get_company_service()
    update_schema = CompanyUpdateSchema(**data['update_company'])
    result = await service.update(update_schema)

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

    company = await service.get(uuid=update_schema.uuid)

    if isinstance(company, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    await state.clear()
    await manage(
        message=message, lang=lang, state=state, company=company,
        edit_text=False
    )


@router.callback_query(
    StateFilter(router_state),
    F.data == FSMCompanyUpdate.miss_button
)
async def miss_state(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:miss_state'
    logger.info(state_handler)

    data = await state.get_data()
    if await st.is_debag():
        logger.info(f'{state_handler} {data=}')

    service = get_company_service()
    update_schema = CompanyUpdateSchema(**data['update_company'])
    result = await service.update(update_schema)

    if isinstance(result, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await callback.message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    terminology_lang: Lang = getattr(terminology, lang)

    await callback.message.answer(
        text=terminology_lang.terms.done
    )

    company = await service.get(uuid=update_schema.uuid)

    if isinstance(company, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await callback.message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    await state.clear()
    await manage(
        message=callback.message, lang=lang, state=state, company=company,
        edit_text=True
    )


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
        *FSMCompanyUpdate.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.error,
        reply_markup=keyboard
    )
