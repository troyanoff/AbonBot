import logging

from aiogram import Router

from routers.clients.create.state import states_group
from filters.general import CallbackFilter
from handlers.create.base import CreateConfig, CreateFieldClb
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.sex

config = CreateConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    term=terminology,
    field_filter=CallbackFilter(
        {
            'm': 'm',
            'f': 'f'
        }
    )
)

handler = CreateFieldClb(
    config=config
)
