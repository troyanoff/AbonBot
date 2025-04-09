import logging

from aiogram import Router
from handlers.representation.base import ReprBase, ReprConfig
from services.actions import get_action_service
from routers.actions.representation.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.repr

config = ReprConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='action',
    service_caller=get_action_service,
    term=terminology,
    next_state_caller='routers.actions.manage.handler',
    item_name=['name'],
    back_button='back_state',
    format_caption={'company_name': 'company_name'},
    callbacks={
        'create': 'routers.actions.create.handler'
    },
)

handler = ReprBase(
    config=config
)
