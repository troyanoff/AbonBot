import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, Message
)

from core.config import settings as st
from handlers.manage.base import ManageBase, ManageConfig
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

config = ManageConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_uuid_key='company_uuid',
    service_caller=get_company_service,
    back_state_caller='routers.companies.representation.default_handler',
    term=terminology,
    callbacks={
        'locations': 'routers.locations.representation.default_handler',
        'actions': 'routers.actions.representation.default_handler',
        'instructors': 'routers.instructors.representation.default_handler',
        'cards': 'routers.cards.representation.default_handler',
        'subscriptions':
            'routers.subscriptions.representation.default_handler',
        'update': 'routers.companies.update.start_handler',
    }
)

handler = ManageBase(
    config=config
)
