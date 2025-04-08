import logging

from aiogram import Router
from handlers.representation.base import ReprBase, ReprConfig
from services.locations import get_location_service
from routers.locations.manage.state_routers.default.handlers \
    import location_count
from routers.locations.representation.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.repr

config = ReprConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='location',
    service_caller=get_location_service,
    term=terminology,
    next_state_caller='routers.locations.manage.handler',
    item_name=['name'],
    back_button='back_state',
    format_caption={'company_name': 'company_name'},
    callbacks={
        'create': 'routers.locations.create.handler'
    },
    callbacks_validate={
        'create': (location_count, 'forbitten')
    },
)

handler = ReprBase(
    config=config
)
