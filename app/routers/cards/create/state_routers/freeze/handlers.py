import logging

from aiogram import Router

# from core.config import settings as st
from routers.cards.create.state import states_group
from schemas.base import CreateFieldEnum
from utils.create_item import CreateConfig, CreateFieldBool
from .terminology import terminology
from ..location.handlers import repr_items


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.freeze
next_state = (states_group.freezing_days, states_group.location)

config = CreateConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    field_type=CreateFieldEnum.default,
    data_field=states_group.data_field,
    term=terminology,
    next_state=next_state,
    end_caller=repr_items.repr,
)
handler = CreateFieldBool(
    config=config,
    buttons=((), ()),
    end_caller_callback='no'
)
