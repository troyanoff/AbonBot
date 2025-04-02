
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, InputMediaPhoto
)
from aiogram.utils.keyboard import InlineKeyboardMarkup
from dataclasses import dataclass
from logging import Logger
from pydantic import BaseModel
from types import CoroutineType

from core.terminology import terminology as core_term, Lang as core_Lang
from handlers.base import RequestTG, Term
from keyboards.inline.base import create_simply_inline_kb
from services.base import BaseService
from utils.support import bad_response
from utils.terminology import LangListBase, LangBase


@dataclass
class ManageConfig:
    logger: Logger
    router: Router
    states_group: StatesGroup
    router_state: State
    item_uuid_key: str
    format: dict
    service_caller: CoroutineType
    back_state_caller: CoroutineType
    back_item_uuid_key: str
    term: LangListBase
    callbacks: dict  # {'callback_name': caller}
    stug_photo_name: str = 'default'


class ManageBase:
    request: RequestTG = None
    term: Term = None

    def __init__(
        self,
        config: ManageConfig
    ):
        self.config = config
        self.service: BaseService = self.config.service_caller()
        self._register_handlers()

    def _register_handlers(self):
        for callback_name in self.config.callbacks:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data == callback_name
            )(self.callback_caller)

        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.in_(('back_state', 'cancel'))
        )(self.back_state)

    def _register_request(
        self,
        handler_name: str,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext
    ):
        state_handler = f'{self.config.router_state.state}:{handler_name}'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
        self.request = RequestTG(callback=callback, lang=lang, state=state)
        terminology_lang: LangBase = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)
        self.term = Term(core=core_term_lang, local=terminology_lang)

    async def create_keyboards(self) -> InlineKeyboardMarkup:
        lang = self.request.lang
        terminology_lang: LangBase = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)

        buttons = terminology_lang.buttons.__dict__
        core_buttons = await core_term_lang.buttons.get_dict_with(
            *self.config.states_group.core_buttons)
        buttons.update(core_buttons)

        keyboard = await create_simply_inline_kb(
            buttons,
            1
        )
        return keyboard

    async def create_caption(self, item: BaseModel):
        lang = self.request.lang
        terminology_lang: LangBase = getattr(self.config.term, lang)
        content = {k: getattr(item, v) for k, v in self.config.format}
        result = terminology_lang.terms.manage_content.format(**content)
        return result

    async def __call__(
        self,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext
    ):
        self.request = self._register_request(
            handler_name='__call__', callback=callback, lang=lang, state=state)

        data = self.request.state.get_data()
        uuid = data[self.config.item_uuid_key]
        item = await self.service.get(uuid=uuid)
        if await bad_response(item, **self.request):
            return

        text = await self.create_caption(item)
        keyboard = await self.create_keyboards()
        media = getattr(self.term.core.photos, self.config.stug_photo_name)

        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=media,
                caption=text
            ),
            reply_markup=keyboard
        )

    async def callback_caller(
        self,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext
    ):
        self.request = RequestTG(callback=callback, lang=lang, state=state)
        state_handler = f'{self.config.router_state.state}:{callback.data}'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
        await self.config.callbacks[callback.data](**self.request)
