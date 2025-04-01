import logging

from aiogram import Router

# from core.config import settings as st
from routers.cards.create.state import states_group
from schemas.base import CreateFieldEnum
from utils.create_item import CreateConfig, CreateFieldBool
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.by_limit
next_state = (states_group.time_limit, states_group.freeze)

config = CreateConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    field_type=CreateFieldEnum.default,
    data_field=states_group.data_field,
    term=terminology,
    next_state=next_state
)
handler = CreateFieldBool(
    config=config,
    buttons=((), ('yes', 'no'))
)
