import logging

from aiogram import Router
from handlers.representation.base import ReprBase, ReprConfig
from services.instructors import get_instructor_service
from routers.instructors.representation.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.repr

config = ReprConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='instructor',
    service_caller=get_instructor_service,
    term=terminology,
    next_state_caller='routers.instructors.manage.handler',
    item_name=['client.first_name', 'client.last_name'],
    back_button=states_group.back_button,
    format_caption={'company_name': 'company_name'},
    callbacks={
        # 'create': 'routers.subscriptions.create.handler'
    },
)

handler = ReprBase(
    config=config
)
