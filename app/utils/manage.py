
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, Message, InputMediaPhoto
)
from dataclasses import dataclass
from logging import Logger
from pydantic import BaseModel
from types import CoroutineType

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb, pages_inline_kb
from routers.default.state import FSMDefault
from schemas.base import BaseReprListSchema
from schemas.utils import FailSchema
from services.base import BaseService
from utils.support import bad_response
from utils.terminology import LangListBase, LangBase


@dataclass
class ManageConfig:
    logger: Logger
    router: Router
    states_group: StatesGroup
    router_state: State
    format: dict
    service_caller: CoroutineType
    back_state_caller: CoroutineType
    back_item_uuid_key: str
    term: LangListBase
    stug_photo_name: str = 'default'


class ManageBase:
    request: RequestTG = None

    def __init__(
        self,
        config: ReprConfig
    ):
        self.config = config
        self.service: BaseService = self.config.service_caller()
        self._register_handlers()

    def _register_handlers(self):
        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.in_(('back_state', 'cancel'))
        )(self.back_state)

        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.regexp((r'^back:\d+:\d+$'))
        )(self.back)

        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.regexp((r'^forward:\d+:\d+$'))
        )(self.forward)

        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.regexp((
                    r'^'
                    + f'{self.config.callback_prefix}'
                    + r':[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab]'
                    + r'[0-9a-f]{3}-[0-9a-f]{12}$'
                ))
        )(self.choice_item)
