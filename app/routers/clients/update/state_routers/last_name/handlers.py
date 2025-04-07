import logging

from aiogram import Router

from core.config import settings as st
from routers.clients.update.state import states_group
from filters.general import TextAlphaFilter
from handlers.create.base import CreateConfig, CreateFieldMsg
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.last_name

config = CreateConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    term=terminology,
    field_filter=TextAlphaFilter(st.short_field_len),
    back_button=states_group.cancel_button,
    miss_button=states_group.miss_button
)

handler = CreateFieldMsg(
    config=config
)
