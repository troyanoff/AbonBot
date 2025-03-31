import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, Message
)

from core.config import settings as st
from routers.cards.manage.state_routers.default.handlers \
    import manage as manage_card
from routers.companies.manage.state_routers.default.handlers \
    import manage as manage_company
from services.cards import get_card_service
from routers.cards.representation.state import states_group
from utils.repr import RerpBase
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.repr
callback_prefix = 'card'

repr_items = RerpBase(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    service_caller=get_card_service,
    manage_caller=manage_card,
    back_manage_caller=manage_company,
    back_manage_uuid='company_uuid',
    back_manage_update_type=Message,
    term=terminology,
    callback_prefix=callback_prefix,
    item_name=['name'],
    stug_photo=st.stug_photo
)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'create'
)
async def create(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:create'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
    from routers.cards.create.state_routers.name.handlers \
        import handler

    await handler.start(callback=callback, state=state, lang=lang)
