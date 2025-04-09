import logging

from aiogram import Router

from handlers.manage.base import ManageBase, ManageConfig
from services.actions import get_action_service
from routers.actions.manage.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.manage


config = ManageConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='action',
    service_caller=get_action_service,
    term=terminology,
    callbacks={
        'archive': 'self.archive',
        'create': 'routers.actions.create.handler',
    },
    format_caption={
        'name': 'name',
        'description': 'description',
    },
    back_button='back_state'
)

handler = ManageBase(
    config=config
)
