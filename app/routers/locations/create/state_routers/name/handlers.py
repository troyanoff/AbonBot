import logging

from aiogram import Router

from core.config import settings as st
from handlers.create import CreateFieldStr, CreateConfig
from routers.locations.create.state import states_group
from schemas.base import CreateFieldEnum
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.name
next_state = states_group.description

config = CreateConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    field_type=CreateFieldEnum.start,
    data_field=states_group.data_field,
    term=terminology,
    next_state=next_state
)
handler = CreateFieldStr(
    config=config,
    max_lengh=st.short_field_len
)
