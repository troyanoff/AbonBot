import logging

from aiogram import Router

from handlers.manage.base import ManageBase, ManageConfig
from services.clients import get_client_service
from routers.clients.profile.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.profile

config = ManageConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='client',
    service_caller=get_client_service,
    term=terminology,
    callbacks={
        'update_profile': 'routers.clients.update.handler',
        'create_company': 'routers.actions.representation.default_handler',
    },
    format_caption={
        'first_name': 'first_name',
        'last_name': 'last_name',
        'sex': 'sex',
    }
)

handler = ManageBase(
    config=config
)
