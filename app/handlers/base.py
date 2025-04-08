from abc import ABC, abstractmethod
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, Message, InputMediaPhoto, InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dataclasses import dataclass, field
from importlib import import_module
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
    photo: str = None
    keyboard: InlineKeyboardMarkup | None = None
    state_instance: dict = None


@dataclass
class RequestTG:
    update: CallbackQuery | Message
    lang: str
    state: FSMContext
    kwargs: dict = field(default_factory=lambda: {})


@dataclass
class Term:
    core: core_Lang
    local: LangBase


@dataclass
class Data:
    request: RequestTG
    term: Term


async def create_request_tg(
    handler_name: str,
    update: CallbackQuery | Message,
    lang: str,
    state: FSMContext,
    logger: Logger,
    **kwargs
) -> RequestTG:
    repr_state = await state.get_state()
    state_handler = f'{repr_state}:{handler_name}'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    return RequestTG(
        update=update, lang=lang, state=state, kwargs=kwargs
    )


@dataclass
class BaseConfig:
    logger: Logger
    router: Router
    states_group: StatesGroup
    router_state: State
    item_prefix: str
    service_caller: CoroutineType
    term: LangListBase
    next_state_caller: str = None
    list_filter: dict = field(default_factory=lambda: {
        'company_uuid': 'company_uuid'
    })
    callbacks: dict = field(default_factory=lambda: {})
    callbacks_validate: dict = field(default_factory=lambda: {})
    stug_photo_name: str = 'default'
    back_button: str = None


class BaseHandler(ABC):
    def __init__(self, config: BaseConfig):
        self.config = config
        self._register_handlers()

    def _register_handlers(self):
        if self.config.callbacks:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data.in_(self.config.callbacks)
            )(self.callback_caller)

        if self.config.back_button:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data == self.config.back_button
            )(self.to_last_state)

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
        term = Term(core=core_term_lang, local=terminology_lang)
        return Data(request=request, term=term)

    def _update_to_request_data(
        self,
        handler_name: str,
        request_tg: RequestTG
    ) -> Data:
        state_handler = f'{self.config.router_state.state}:{handler_name}'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
        terminology_lang: LangBase = getattr(self.config.term, request_tg.lang)
        core_term_lang: core_Lang = getattr(core_term, request_tg.lang)
        term = Term(core=core_term_lang, local=terminology_lang)
        return Data(request=request_tg, term=term)

    async def _get_count(self, data: Data):
        state_data = await data.request.state.get_data()
        return state_data

    async def create_inline_kb(
        self,
        buttons: dict,
        width: int
    ) -> InlineKeyboardMarkup:
        kb_builder = InlineKeyboardBuilder()
        kb_buttons: list[InlineKeyboardButton] = []
        for button, value in buttons.items():
            kb_buttons.append(InlineKeyboardButton(
                text=value,
                callback_data=button))

        kb_builder.row(*kb_buttons, width=width)
        return kb_builder.as_markup()

    async def create_simply_kb(
        self, data: Data
    ) -> InlineKeyboardMarkup:
        buttons = data.term.local.buttons.__dict__

        back_reason = await self.back_state_group_exist(data)
        if back_reason and self.config.back_button:
            core_buttons = await data.term.core.buttons.get_dict_with(
                self.config.back_button)
            buttons.update(core_buttons)

        keyboard = await self.create_inline_kb(buttons, 1)
        return keyboard

    async def _create_keyboard(self, data: Data) -> InlineKeyboardMarkup:
        pass

    async def _create_caption(self, data: Data, item: BaseModel) -> str:
        pass

    async def _choise_media(self, data: Data, item: BaseModel) -> str:
        pass

    async def get_state_key(self, data: Data, key: str):
        state_data = await data.request.state.get_data()
        return state_data.get(key)

    async def choise_message(self, data: Data) -> Message:
        if isinstance(data.request.update, CallbackQuery):
            return data.request.update.message
        return data.request.update

    async def choise_caller(
        self, caller_entity: str | CoroutineType
    ) -> CoroutineType:
        if isinstance(caller_entity, CoroutineType):
            return caller_entity
        module_path, caller = caller_entity.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, caller)

    async def next_state_group(self, data: Data):
        now_state = await data.request.state.get_state()
        if now_state == self.config.router_state:
            return
        await data.request.state.set_state(self.config.router_state)
        last_message_json = await self.get_state_key(data, 'last_message')
        if not last_message_json:
            await data.request.state.update_data(state_path=[])
            return
        state_path: list = await self.get_state_key(data, 'state_path')
        state_path.append(last_message_json)
        await data.request.state.update_data(state_path=state_path)

    async def back_state_group_exist(self, data: Data):
        state_path = await self.get_state_key(data, 'state_path')
        return bool(state_path)

    async def back_state_group(self, data: Data):
        state_path: list = await self.get_state_key(data, 'state_path')
        last_message = LastMessage.model_validate_json(state_path.pop())
        await data.request.state.update_data(state_path=state_path)
        await data.request.state.set_state(last_message.state)
        await data.request.state.set_data(last_message.state_instance)
        return last_message

    async def answer(self, data: Data, last_message: LastMessage):
        msg = await self.choise_message(data)

        if msg.from_user.id != await st.get_bot_id():
            await msg.answer_photo(
                photo=last_message.photo,
                caption=last_message.text,
                reply_markup=last_message.keyboard
            )
            return

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

    async def equals_messages(self, old: LastMessage, new: LastMessage):
        return all(
            (old.state == new.state,
             old.text == new.text,
             old.photo == new.photo,
             old.keyboard == new.keyboard)
        )

    async def remember_answer(self, data: Data, last_message: LastMessage):
        now_last_message = await self.get_state_key(data, 'last_message')
        if now_last_message:
            now_last_message_model = LastMessage.model_validate_json(
                now_last_message
            )
            equals = await self.equals_messages(
                now_last_message_model, last_message)
            if equals:
                return
        await data.request.state.update_data(
            last_message=last_message.model_dump_json())

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
            return True

    @abstractmethod
    async def __call__(
        self,
        update: CallbackQuery | Message,
        lang: str,
        state: FSMContext
    ):
        pass

    async def to_last_state(
        self,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext
    ):
        data: Data = self._get_request_data(
            'to_last_state', callback, lang, state
        )
        reason = await self.back_state_group_exist(data)
        if not reason:
            return
        last_message = await self.back_state_group(data)
        await self.remember_answer(data, last_message)
        await self.answer(data, last_message)

    async def callback_caller(
        self,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext
    ):
        data: Data = self._get_request_data(
            'callback_caller', callback, lang, state
        )
        if callback.data in self.config.callbacks_validate:
            check_valid_callback, phrase = self.config.callbacks_validate[
                callback.data]
            valid = await check_valid_callback(data)
            if not valid:
                await callback.answer(
                    getattr(data.term.local.terms, phrase),
                    show_alert=True
                )
                return
        await callback.answer()
        caller = await self.choise_caller(self.config.callbacks[callback.data])
        await caller(data.request)
