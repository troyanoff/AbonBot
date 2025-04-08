import logging

from aiogram import Router

from routers.companies.create.state import states_group
from filters.general import EmailFilter
from handlers.create.base import CreateConfig, CreateFieldMsg
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.email

config = CreateConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    term=terminology,
    field_filter=EmailFilter(),
    back_button=states_group.cancel_button
)

handler = CreateFieldMsg(
    config=config
)
