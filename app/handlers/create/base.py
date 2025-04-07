
from aiogram import Router, F
from aiogram.filters import StateFilter, BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, Message
)
from aiogram.utils.keyboard import InlineKeyboardMarkup
from dataclasses import dataclass, field
from logging import Logger
from typing import Any

from core.config import settings as st
from handlers.base import BaseHandler, Data, RequestTG
from utils.terminology import LangListBase


@dataclass
class CreateConfig:
    logger: Logger
    router: Router
    states_group: StatesGroup
    router_state: State
    term: LangListBase
    field_filter: BaseFilter
    callbacks: dict = field(default_factory=lambda: {})
    back_button: str = None
    miss_button: str = None


class CreateField(BaseHandler):
    def __init__(
        self,
        config: CreateConfig,
    ):
        self.config = config
        self.handler = None
        self._register_handlers()

    def _register_handlers(self):
        pass

    async def update_data(self, data: Data, result: Any | dict):
        field_name = self.config.router_state.state.split(st.state_sep)[-1]

        state_data = await data.request.state.get_data()
        data_field_dict: dict = state_data[self.handler.config.generated_field]
        if isinstance(result, dict):
            data_field_dict.update(result)
        else:
            data_field_dict[field_name] = result

        await data.request.state.update_data(
            {self.handler.config.generated_field: data_field_dict}
        )

        if await st.is_debag():
            state_data = await data.request.state.get_data()
            self.config.logger.info(f'\n{'=' * 80}\n{state_data}\n{'=' * 80}')

    async def choise_message_method(self, data: Data, msg: Message):
        if isinstance(data.request.update, CallbackQuery):
            return msg.answer
        else:
            return msg.answer

    async def answer(
        self, data: Data, text: str, keyboard: InlineKeyboardMarkup | None
    ):
        msg = await self.choise_message(data)
        msg_method = await self.choise_message_method(data, msg)

        await msg_method(
            text=text,
            reply_markup=keyboard
        )

    async def create_simply_kb(
        self, data: Data
    ) -> InlineKeyboardMarkup:
        buttons = data.term.local.buttons.__dict__

        if self.config.miss_button:
            core_buttons = await data.term.core.buttons.get_dict_with(
                self.config.miss_button)
            buttons.update(core_buttons)

        back_reason = await self.back_state_group_exist(data)
        if back_reason:
            core_buttons = await data.term.core.buttons.get_dict_with(
                self.config.back_button)
            buttons.update(core_buttons)

        keyboard = await self.create_inline_kb(buttons, 1)
        return keyboard

    async def _create_keyboard(self, data: Data):
        return await self.create_simply_kb(data)

    async def __call__(
        self, request_tg: RequestTG
    ):
        data: Data = self._update_to_request_data('call', request_tg)
        keyboard = await self._create_keyboard(data)
        text = data.term.local.terms.call
        await self.answer(data, text, keyboard)

    async def miss(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        data: Data = self._get_request_data(
            'miss', callback, lang, state
        )
        await self.handler.next_state(data.request)


class CreateFieldMsg(CreateField):
    def __init__(
        self,
        config: CreateConfig,
    ):
        self.config = config
        self.handler = None
        self._register_handlers()

    def _register_handlers(self):
        self.config.router.message(
            StateFilter(self.config.router_state),
            self.config.field_filter
        )(self.done)

        self.config.router.message(
            StateFilter(self.config.router_state)
        )(self.error)

        if self.config.callbacks:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data.in_(self.config.callbacks)
            )(self.callback_caller)

        if self.config.miss_button:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data == self.config.miss_button
            )(self.miss)

        if self.config.back_button:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data == self.config.back_button
            )(self.to_last_state)

    async def done(
        self,
        message: Message,
        state: FSMContext,
        lang: str,
        result: dict | Any
    ):
        data: Data = self._get_request_data(
            'done', message, lang, state
        )
        await self.update_data(data, result)
        await self.handler.next_state(data.request)

    async def error(
        self, message: Message, lang: str, state: FSMContext
    ):
        data: Data = self._get_request_data(
            'error', message, lang, state
        )
        keyboard = await self._create_keyboard(data)
        text = data.term.local.terms.error
        await self.answer(data, text, keyboard)


class CreateFieldClb(CreateField):
    def __init__(
        self,
        config: CreateConfig,
    ):
        self.config = config
        self.handler = None
        self._register_handlers()

    def _register_handlers(self):
        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            self.config.field_filter
        )(self.callback_caller)

        if self.config.miss_button:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data == self.config.miss_button
            )(self.miss)

        if self.config.back_button:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data == self.config.back_button
            )(self.to_last_state)

        self.config.router.message(
            StateFilter(self.config.router_state)
        )(self.error)

    async def callback_caller(
        self,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext,
        result: Any | dict
    ):
        data: Data = self._get_request_data(
            'callback_caller', callback, lang, state
        )
        await self.update_data(data, result)
        await self.handler.next_state(data.request)

    async def error(
        self, message: Message, lang: str, state: FSMContext
    ):
        data: Data = self._get_request_data(
            'error', message, lang, state
        )
        keyboard = await self._create_keyboard(data)
        text = data.term.local.terms.error
        await self.answer(data, text, keyboard)
