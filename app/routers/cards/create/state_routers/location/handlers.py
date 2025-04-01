import logging

from aiogram import Router
from aiogram.types import (
    CallbackQuery, Message
)

from core.config import settings as st
from routers.companies.manage.state_routers.default.handlers \
    import manage as manage_company
from services.locations import get_location_service
from routers.cards.create.state import states_group
from utils.repr import RerpBase
from .terminology import terminology
from ..actions.handlers import repr_items


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.location
callback_prefix = 'location'

repr_items = RerpBase(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    service_caller=get_location_service,
    manage_caller=repr_items.repr,
    back_manage_caller=manage_company,
    back_manage_uuid='company_uuid',
    back_manage_update_type=Message,
    term=terminology,
    callback_prefix=callback_prefix,
    item_name=['name'],
    stug_photo=st.stug_photo,
    manage_caller_update_type=CallbackQuery
)
