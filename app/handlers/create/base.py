
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, Message
)
from aiogram.utils.keyboard import InlineKeyboardMarkup
from logging import Logger
from types import CoroutineType

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from handlers.base import RequestTG, Term
from keyboards.inline.base import create_simply_inline_kb
from schemas.base import CreateFieldEnum
from utils.terminology import LangBase


class CreateConfig:
    def __init__(
        self,
        logger: Logger,
        router: Router,
        states_group: StatesGroup,
        router_state: State,
        field_type: CreateFieldEnum,
        data_field: str,
        term,
        need_last_buttons: bool = False,
        last_buttons: tuple = None,
        last_term=None,
        next_state: State | tuple = None,
        end_caller: CoroutineType = None
    ):
        self.router = router
        self.logger = logger
        self.states_group = states_group
        self.router_state = router_state
        self.field_type = field_type
        self.data_field = data_field
        self.term = term
        self.need_last_buttons = need_last_buttons
        self.last_buttons = last_buttons
        self.last_term = last_term
        self.next_state = next_state
        self.end_caller = end_caller


class CreateField:
    def __init__(
        self,
        config: CreateConfig,
    ):
        self.config = config
        self.request: RequestTG = None
        self.term: Term = None
        self._register_handlers()

    def _register_mutable_handlers(self):
        self.config.router.message(
            StateFilter(self.config.router_state),
            F.text.len() <= st.short_field_len
        )(self.done)

    def _register_handlers(self):
        self._register_mutable_handlers()

        self.config.router.message(
            StateFilter(self.config.router_state)
        )(self.error)

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
        if self.config.last_term:
            last_term_lang: LangBase = getattr(self.config.last_term, lang)
            self.term.last_local = last_term_lang

    async def choise_message(self):
        if isinstance(self.request.update, CallbackQuery):
            return self.request.update.message
        return self.request.update

    async def update_data(self):
        field_name = self.config.router_state.state.split(st.state_sep)[-1]
        data = await self.request.state.get_data()
        data_field_dict = data[self.config.data_field]
        data_field_dict[field_name] = self.request.update.text
        await self.request.state.update_data(
            {self.config.data_field: data_field_dict}
        )
        if await st.is_debag():
            data = await self.request.state.get_data()
            self.config.logger.info(f'\n{'=' * 80}\n{data}\n{'=' * 80}')

    async def done_keyboard(self) -> InlineKeyboardMarkup:

        buttons = self.term.local.buttons.__dict__
        core_buttons = await self.term.core.buttons.get_dict_with(
            *self.config.states_group.core_buttons)
        buttons.update(core_buttons)

        keyboard = await create_simply_inline_kb(
            buttons,
            1
        )

        return keyboard

    async def error_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        if self.config.last_term:
            buttons = await self.term.last_local.buttons.get_dict_with(
                *self.config.last_buttons
            )
            core_buttons = await self.term.core.buttons.get_dict_with(
                *self.config.states_group.core_buttons)
            buttons.update(core_buttons)
        else:
            buttons = await self.term.core.buttons.get_dict_with(
                *self.config.states_group.core_buttons)

        keyboard = await create_simply_inline_kb(
            buttons,
            1
        )

        return keyboard

    async def done_end(
        self,
        update: Message | CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        keyboard = await self.done_keyboard()

        await update.answer(
            text=self.term.local.terms.done,
            reply_markup=keyboard
        )
        await state.set_state(self.config.next_state)

    async def __call__(
        self, update: CallbackQuery | Message, state: FSMContext, lang: str
    ):
        self._register_request(
            handler_name='__call__',
            update=update,
            lang=lang,
            state=state
        )
        data = await state.get_data()

        await update.answer()
        await state.update_data(
            {
                self.config.data_field: {
                    'company_uuid': data['company_uuid']
                }
            }
        )

        core_buttons = await self.term.core.buttons.get_dict_with(
            *self.config.states_group.core_buttons)

        keyboard = await create_simply_inline_kb(
            core_buttons,
            1
        )
        msg = await self.choise_message()
        await msg.answer(
            text=self.term.local.terms.start,
            reply_markup=keyboard
        )
        await state.set_state(self.config.router_state)

    async def done(
        self, message: Message, state: FSMContext, lang: str
    ):
        self._register_request(
            handler_name='done',
            update=message,
            lang=lang,
            state=state
        )

        await self.update_data()

        done_func = self.done_end
        if self.config.end_caller:
            done_func = self.config.end_caller
        await done_func(message, state, lang)

    async def error(
        self, message: Message, lang: str, state: FSMContext
    ):
        self._register_request(
            handler_name='error',
            update=message,
            lang=lang,
            state=state
        )

        keyboard = await self.error_keyboard(lang)

        await message.answer(
            text=self.term.local.terms.error,
            reply_markup=keyboard
        )
