import logging

from aiogram import Router
from handlers.representation.base import ReprBase, ReprConfig
from services.companies import get_company_service
from routers.companies.representation.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.repr
next_state_caller = (
    'routers.companies.manage.handler'
)

config = ReprConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    service_caller=get_company_service,
    next_state_caller=next_state_caller,
    term=terminology,
    item_prefix='company',
    item_name=['name'],
    list_filter={
        'creator_uuid': 'client_uuid'
    }
)

handler = ReprBase(
    config=config
)
