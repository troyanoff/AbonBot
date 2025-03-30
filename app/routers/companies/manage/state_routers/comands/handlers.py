import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    Message, CallbackQuery
)

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import (
    create_simply_inline_kb, create_offset_inline_kb
)
from routers.locations.manage.state_routers.default.handlers import manage
from services.locations import get_location_service
from routers.companies.manage.state import FSMCompanyManage
from schemas.utils import FailSchema
from schemas.representations import (
    CompanyReprSchema,
    LocationListSchema
)
# from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMCompanyManage.manage
callback_prefix = 'company'


@router.callback_query(
    StateFilter(router_state),
    F.data == 'locations'
)
async def locations(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    from routers.locations.representation.state_routers.repr.handlers \
        import locations_repr
    state_handler = f'{router_state.state}:locations'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
    await locations_repr(message=callback.message, lang=lang, state=state)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'actions'
)
async def actions(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    from routers.actions.representation.state_routers.repr.handlers \
        import start
    state_handler = f'{router_state.state}:actions'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    await start(callback=callback, lang=lang, state=state)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'subscriptions'
)
async def subscriptions(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    from routers.subscriptions.representation_company.state_routers.repr.\
        handlers import start
    state_handler = f'{router_state.state}:subscriptions'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    await start(message=callback.message, lang=lang, state=state)
