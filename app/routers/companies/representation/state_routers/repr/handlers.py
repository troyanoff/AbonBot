import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, Message
)

from core.config import settings as st
from handlers.representation.base import ReprBase, ReprConfig
from routers.locations.manage.state_routers.default.handlers \
    import manage as manage_location
from routers.companies.manage.state_routers.default.handlers \
    import manage as manage_company
from services.companies import get_company_service
from routers.locations.representation.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.repr
callback_prefix = 'company'

config = ReprConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    service_caller=get_company_service,
    next_state_caller=handler,
    term=terminology,
    callback_prefix='company',
    item_name=['name']
)

handler = ReprBase(
    config=config
)
