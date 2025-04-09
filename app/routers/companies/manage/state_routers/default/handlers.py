import logging

from aiogram import Router

from handlers.manage.base import ManageBase, ManageConfig
from services.companies import get_company_service
from routers.companies.manage.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.manage

config = ManageConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='company',
    service_caller=get_company_service,
    term=terminology,
    callbacks={
        'locations': 'routers.locations.representation.handler',
        'actions': 'routers.actions.representation.handler',
        'instructors': 'routers.instructors.representation.handler',
        'cards': 'routers.cards.representation.handler',
        'subscriptions':
            'routers.subscriptions.representation.handler',
        'update': 'routers.companies.update.handler',
    },
    format_caption={
        'name': 'name',
        'description': 'description',
        'email': 'email',
        'max_hour_cancel': 'max_hour_cancel',
    },
    back_button='back_state'
)

handler = ManageBase(
    config=config
)
