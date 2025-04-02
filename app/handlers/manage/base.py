
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, InputMediaPhoto, Message
)
from aiogram.utils.keyboard import InlineKeyboardMarkup
from dataclasses import dataclass
from importlib import import_module
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
    item_prefix: str
    format: dict
    service_caller: CoroutineType
    back_state_callers: tuple[str | None, str | None]  # one item, many items
    term: LangListBase
    callbacks: dict  # {'callback_name': 'path to caller'}
    back_item_uuid_key: str = None
    stug_photo_name: str = 'default'


class ManageBase:

    def __init__(
        self,
        config: ManageConfig
    ):
        self.config = config
        self.request: RequestTG = None
        self._register_handlers()

    def _register_handlers(self):
        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.in_(self.config.callbacks)
        )(self.callback_caller)

        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.in_(('back_state', 'cancel', 'general'))
        )(self.back_state)

    def _register_request(
        self,
        handler_name: str,
        update: CallbackQuery | Message,
        lang: str,
        state: FSMContext
    ):
        state_handler = f'{self.config.router_state.state}:{handler_name}'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
        self.request = RequestTG(update=update, lang=lang, state=state)
        terminology_lang: LangBase = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)
        self.term = Term(core=core_term_lang, local=terminology_lang)
        print(self.request, '2' * 1000)

    async def _get_state_key(self, key: str):
        data = await self.request.state.get_data()
        return data[key]

    async def _get_count(self):
        data = await self.request.state.get_data()
        return data[f'{self.config.item_prefix}_count']

    async def create_keyboards(self) -> InlineKeyboardMarkup:
        lang = self.request.lang
        terminology_lang: LangBase = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)

        buttons = terminology_lang.buttons.__dict__

        count = await self._get_count()
        if ((count > 1 and self.config.back_state_callers[1])
                or (count == 1 and self.config.back_state_callers[0])):
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
        content = {k: getattr(item, v) for k, v in self.config.format.items()}
        result = terminology_lang.terms.manage_content.format(**content)
        return result

    async def __call__(
        self,
        update: CallbackQuery | Message,
        lang: str,
        state: FSMContext
    ):
        self._register_request(
            handler_name='__call__', update=update, lang=lang, state=state)
        await state.set_state(self.config.router_state)

        data = await self.request.state.get_data()
        uuid = data[f'{self.config.item_prefix}_uuid']
        service: BaseService = self.config.service_caller()
        item = await service.get(uuid=uuid)
        if await bad_response(item, **self.request.__dict__):
            return

        text = await self.create_caption(item)
        keyboard = await self.create_keyboards()
        media = getattr(self.term.core.photos, self.config.stug_photo_name)

        if isinstance(self.request.update, CallbackQuery):
            msg = self.request.update.message
        else:
            msg = self.request.update
        if msg.photo:
            await msg.edit_media(
                media=InputMediaPhoto(
                    media=media,
                    caption=text
                ),
                reply_markup=keyboard
            )
        else:
            await msg.answer_photo(
                photo=media,
                caption=text,
                reply_markup=keyboard
            )

    async def callback_caller(
        self,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext
    ):
        self._register_request(
            handler_name=callback.data,
            update=callback,
            lang=lang,
            state=state
        )
        module_path, caller = self.config.callbacks[
            callback.data].rsplit('.', 1)
        module = import_module(module_path)
        await getattr(module, caller)(**self.request.__dict__)
        await self.config.callbacks[callback.data](**self.request.__dict__)

    async def back_state(
        self,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext
    ):
        self._register_request(
            handler_name=callback.data,
            update=callback,
            lang=lang,
            state=state
        )
        count = await self._get_count()
        if count > 1:
            path = self.config.back_state_callers[1]
            if path:
                handler = import_module(path)
                uuid_key = self.config.back_item_uuid_key
                if uuid_key:
                    uuid = await self._get_state_key(uuid_key)
                    await handler(uuid=uuid, **self.request.__dict__)
                else:
                    await handler(**self.request.__dict__)
        else:
            path = self.config.back_state_callers[0]
            if path:
                handler = import_module(path)
                await handler(**self.request.__dict__)
