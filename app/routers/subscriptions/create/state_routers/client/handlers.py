import logging

from aiogram import Router

from routers.subscriptions.create.state import states_group
from filters.general import SubTGIDFilter
from handlers.create.base import CreateConfig, CreateFieldMsg
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.client

config = CreateConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    term=terminology,
    field_filter=SubTGIDFilter(),
    back_button=states_group.back_button
)

handler = CreateFieldMsg(
    config=config
)
