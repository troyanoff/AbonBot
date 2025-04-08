import logging

from aiogram import Router

from routers.locations.update.state import states_group
from filters.general import PhotoFilter
from handlers.create.base import CreateConfig, CreateFieldMsg
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.photo

config = CreateConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    term=terminology,
    field_filter=PhotoFilter(),
    miss_button=states_group.miss_button,
    back_button=states_group.cancel_button
)

handler = CreateFieldMsg(
    config=config
)
