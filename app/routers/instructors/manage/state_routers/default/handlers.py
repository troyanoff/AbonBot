import logging

from aiogram import Router

from handlers.manage.base import ManageBase, ManageConfig
from services.instructors import get_instructor_service
from routers.instructors.manage.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.manage


config = ManageConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='instructor',
    service_caller=get_instructor_service,
    term=terminology,
    callbacks={
        'update': 'routers.instructors.update.handler',
        'archive': 'self.archive'
    },
    format_caption={
        'first_name': 'client.first_name',
        'last_name': 'client.last_name',
        'sex': 'client.sex'
    },
    back_button=states_group.back_button
)

handler = ManageBase(
    config=config
)
