from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, Message, InputMediaPhoto, InlineKeyboardMarkup
)
from dataclasses import dataclass, field
from logging import Logger
from pydantic import BaseModel
from types import CoroutineType

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from schemas.base import MyBaseModel
from schemas.utils import DoneSchema, FailSchema
from utils.terminology import LangBase, LangListBase


class LastMessage(MyBaseModel):
    state: str
    text: str
    photo: str
    keyboard: InlineKeyboardMarkup | None


class LastMessageList(MyBaseModel):
    queue: list[LastMessage]


@dataclass
class RequestTG:
    update: CallbackQuery | Message
    lang: str
    state: FSMContext
    kwargs: dict = field(default_factory=lambda: {})


@dataclass
class Term:
    core: LangBase
    local: LangBase


@dataclass
class TermLast(Term):
    last_local: LangBase = None


@dataclass
class Data:
    request: RequestTG
    term: Term | TermLast


@dataclass
class BaseConfig:
    logger: Logger
    router: Router
    states_group: StatesGroup
    router_state: State
    item_prefix: str
    service_caller: CoroutineType
    next_state_caller: str
    back_state_callers: tuple[str | None, str | None]  # one item, many items
    term: LangListBase
    list_filter: dict = field(default_factory=lambda: {
        'company_uuid': 'company_uuid'
    })
    callbacks: dict = field(default_factory=lambda: {
        # 'callback_name': 'path to caller'
    })
    back_item_uuid_key: str = None
    stug_photo_name: str = 'default'
    last_term: LangListBase = None


class BaseHandler:
    def __init__(self, config: BaseConfig):
        self.config = config

    def _get_request_data(
        self,
        handler_name: str,
        update: CallbackQuery | Message,
        lang: str,
        state: FSMContext,
        **kwargs
    ) -> Data:
        state_handler = f'{self.config.router_state.state}:{handler_name}'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        request = RequestTG(
            update=update, lang=lang, state=state, kwargs=kwargs
        )

        terminology_lang: LangBase = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)
        if self.config.last_term:
            last_term_lang: LangBase = getattr(self.config.last_term, lang)
            term = TermLast(
                core=core_term_lang,
                local=terminology_lang,
                last_local=last_term_lang
            )
        else:
            term = Term(core=core_term_lang, local=terminology_lang)
        return Data(request=request, term=term)

    async def _get_count(self, data: Data):
        state_data = await data.request.state.get_data()
        return state_data

    async def _create_keyboards(self, data: Data) -> InlineKeyboardMarkup:
        pass

    async def _create_caption(self, data: Data, item: BaseModel) -> str:
        pass

    async def _choise_media(self, data: Data, item: BaseModel) -> str:
        pass

    async def get_state_key(self, data: Data, key: str):
        state_data = await data.request.state.get_data()
        return state_data.get(key)

    async def set_state_keys(self, data: Data, **kwargs):
        await data.request.state.update_data(kwargs)

    async def choise_message(self, data: Data) -> Message:
        if isinstance(data.request.update, CallbackQuery):
            return data.request.update.message
        return data.request.update

    async def next_state_group(self, data: Data):
        last_message_json = await self.get_state_key(data, 'last_message')
        if not last_message_json:
            await data.request.state.update_data(state_path=[])
            return
        state_path: list = await self.get_state_key(data, 'state_path')
        state_path.append(last_message_json)
        await self.set_state_keys(data, state_path=state_path)

    async def back_state_group_exist(self, data: Data):
        state_path = await self.get_state_key(data, 'state_path')
        return bool(state_path)

    async def back_state_group(self, data: Data):
        state_path: list = await self.get_state_key(data, 'state_path')
        last_message = LastMessage.model_validate_json(state_path.pop())
        await self.set_state_keys(data, state_path=state_path)
        await data.request.state.set_state(last_message.state)
        return last_message

    async def last_message_remember(
        self, data: Data, last_message: LastMessage
    ):
        now_state = await data.request.state.get_state()
        if now_state != last_message.state:
            await data.request.state.set_state(last_message.state)
        await self.set_state_keys(data, last_message=last_message)

    async def answer(self, data: Data, last_message: LastMessage):
        msg = await self.choise_message(data)

        if msg.photo:
            await msg.edit_media(
                media=InputMediaPhoto(
                    media=last_message.photo,
                    caption=last_message.text
                ),
                reply_markup=last_message.keyboard
            )
        else:
            await msg.answer_photo(
                photo=last_message.photo,
                caption=last_message.text,
                reply_markup=last_message.keyboard
            )

    async def bad_response(
        self,
        data: Data,
        response: DoneSchema | FailSchema
    ) -> bool:
        if isinstance(response, FailSchema):
            text = data.term.core.terms.error
            photo = data.term.core.photos.error
            keyboard = None
            msg = await self.choise_message(data)
            if msg.photo:
                await msg.edit_media(
                    media=InputMediaPhoto(
                        media=photo,
                        caption=text
                    ),
                    reply_markup=keyboard
                )
            else:
                await msg.answer_photo(
                    photo=photo,
                    caption=text,
                    reply_markup=keyboard
                )
            await data.request.state.clear()
            await data.request.state.set_state('FSMDefault:default')
            return
