import logging

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from keyboards.menu.base import set_client_menu
from services.companies import get_company_service
from schemas.representations import ClientReprSchema, CompanyListSchema
from schemas.utils import FailSchema
from routers.clients.update.state import FSMClientUpdate
from routers.default.state import FSMDefault, FSMStart
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


@router.callback_query(
    ~StateFilter(default_state, router_state),
    F.data.in_(('cancelRR', 'general'))
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
