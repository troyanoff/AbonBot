import logging

from aiogram import Router

from handlers.manage.base import ManageBase, ManageConfig
from services.locations import get_location_service
from routers.locations.manage.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.manage

config = ManageConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='location',
    service_caller=get_location_service,
    term=terminology,
    callbacks={
        'update': 'routers.locations.update.start_handler',
        'create': 'routers.locations.create.start_handler',
    },
    format_caption={
        'name': 'name',
        'description': 'description',
        'city': 'city',
        'street': 'street',
        'house': 'house',
        'flat': 'flat',
    },
    back_button='back_state'
)

handler = ManageBase(
    config=config
)
