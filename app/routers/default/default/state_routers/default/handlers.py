import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from keyboards.menu.base import set_client_menu
from services.companies import get_company_service
from states.general import FSMStart
from schemas.representations import ClientReprSchema, CompanyListSchema
from schemas.utils import FailSchema
from routers.clients.update.state import FSMClientUpdate
from routers.default.state import FSMDefault
from routers.companies.create.state_routers.name.handlers import start_create
from routers.companies.representation.state import FSMCompanyRepr
from routers.companies.representation.state_routers.repr.handlers import \
    companies_repr
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMDefault.default


@router.message(CommandStart(), StateFilter(router_state))
async def start(
    message: Message,
    state: FSMContext,
    bot: Bot,
    lang: str,
    client_data: ClientReprSchema | None
):
    state_handler = f'{router_state.state}:start'
    logger.info(state_handler)

    core_term_lang: core_Lang = getattr(core_term, lang)

    if not client_data:
        await message.answer(
            text=core_term_lang.terms.start_unknow
        )
        await state.set_state(FSMStart.start)
        return

    terminology_lang: Lang = getattr(terminology, lang)

    await set_client_menu(bot, client_data.tg_id, core_term_lang.menu)

    await message.answer(
        text=terminology_lang.terms.start
    )


@router.message(Command(commands='companies'), StateFilter(FSMDefault.default))
async def companies_command(
    message: Message,
    lang: str,
    client_data: ClientReprSchema,
    state: FSMContext,
):
    await state.set_state(FSMCompanyRepr.repr)
    await companies_repr(
        message=message, client_data=client_data, state=state, lang=lang)


@router.message(Command(commands='learn'), StateFilter(router_state))
async def learn(
    message: Message,
    lang: str
):
    state_handler = f'{router_state.state}:learn'
    logger.info(state_handler)
    terminology_lang: Lang = getattr(terminology, lang)
    await message.answer(
        text=terminology_lang.terms.learn
    )


@router.message(Command(commands='support'), StateFilter(router_state))
async def support(
    message: Message,
    lang: str
):
    state_handler = f'{router_state.state}:support'
    logger.info(state_handler)
    terminology_lang: Lang = getattr(terminology, lang)
    await message.answer(
        text=terminology_lang.terms.support
    )


@router.message(Command(commands='profile'), StateFilter(router_state))
async def profile(
    message: Message,
    lang: str,
    client_data: ClientReprSchema
):
    state_handler = f'{router_state.state}:profile'
    logger.info(state_handler)

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)
    keyboard = await create_simply_inline_kb(
        buttons=terminology_lang.buttons.__dict__,
        width=1
    )
    sex = getattr(core_term_lang.terms, client_data.sex.name)
    text = terminology_lang.terms.profile.format(
        first_name=client_data.first_name,
        last_name=client_data.last_name,
        sex=sex,
        companies_count=0,  # to do
        subs_count=0  # to do
    )
    if not client_data.photo_id:
        await message.answer(
            text=text,
            reply_markup=keyboard
        )
        return
    await message.answer_photo(
        photo=client_data.photo_id,
        caption=text,
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(router_state),
    F.data == 'update_profile'
)
async def update_profile(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:update_profile'
    logger.info(state_handler)

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    buttons = await core_term_lang.buttons.get_dict_with(
        *FSMClientUpdate.core_buttons)
    keyboard = await create_simply_inline_kb(
        buttons,
        1
    )

    await callback.message.answer(
        text=terminology_lang.terms.update_profile,
        reply_markup=keyboard
    )
    await state.set_state(FSMClientUpdate.first_name)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'create_company'
)
async def create_company(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str,
    client_data: ClientReprSchema
):
    state_handler = f'{router_state.state}:create_company'
    logger.info(state_handler)

    service = get_company_service()
    companies: CompanyListSchema = await service.get_list(
        client_data.uuid)

    if await st.is_debag():
        logger.info(f'{companies=}')

    core_term_lang: core_Lang = getattr(core_term, lang)
    if isinstance(companies, FailSchema):
        await callback.message.answer(
            text=core_term_lang.terms.error
        )
        return

    if companies.total_count > 0 and not client_data.is_premium:
        terminology_lang: Lang = getattr(terminology, lang)
        await callback.message.answer(
            text=terminology_lang.terms.max_companies
        )
        return

    return await start_create(
        message=callback.message, state=state,
        lang=lang, client_data=client_data
    )


@router.callback_query(
    ~StateFilter(default_state, router_state),
    F.data.in_(('cancel', 'general'))
)
async def cancel(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:cancel'
    logger.info(state_handler)

    await callback.message.delete()
    core_term_lang: core_Lang = getattr(core_term, lang)
    await callback.message.answer(
        text=core_term_lang.terms.cancel
    )
    await state.clear()
    await state.set_state(FSMDefault.default)
