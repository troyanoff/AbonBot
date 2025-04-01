import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, Message
)

from core.config import settings as st
from routers.locations.manage.state_routers.default.handlers \
    import manage as manage_location
from routers.companies.manage.state_routers.default.handlers \
    import manage as manage_company
from services.actions import get_action_service
from routers.cards.create.state import states_group
from utils.repr import RerpBase
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.location
callback_prefix = 'action'

repr_items = RerpBase(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    service_caller=get_action_service,
    manage_caller=manage_location,
    back_manage_caller=manage_company,
    back_manage_uuid='company_uuid',
    back_manage_update_type=Message,
    term=terminology,
    callback_prefix=callback_prefix,
    item_name=['name'],
    stug_photo=st.stug_photo
)
