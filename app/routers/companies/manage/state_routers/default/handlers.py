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
    back_state_callers=(
        None,
        'routers.companies.representation.default_handler'
    ),
    term=terminology,
    callbacks={
        'locations': 'routers.locations.representation.default_handler',
        'actions': 'routers.actions.representation.default_handler',
        'instructors': 'routers.instructors.representation.default_handler',
        'cards': 'routers.cards.representation.default_handler',
        'subscriptions':
            'routers.subscriptions.representation.default_handler',
        'update': 'routers.companies.update.start_handler',
    },
    format={
        'name': 'name',
        'description': 'description',
        'email': 'email',
        'max_hour_cancel': 'max_hour_cancel',
    }
)

handler = ManageBase(
    config=config
)
