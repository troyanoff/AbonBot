
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, Message
)
from logging import Logger

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from schemas.base import CreateFieldEnum


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
        next_state: State = None,
    ):
        self.router = router
        self.logger = logger
        self.states_group = states_group
        self.router_state = router_state
        self.field_type = field_type
        self.data_field = data_field
        self.term = term
        self.next_state = next_state


class CreateField:
    def __init__(
        self,
        config: CreateConfig,
    ):
        self.config = config
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

    async def update_data(self, message: Message, state: FSMContext):
        field_name = self.config.router_state.state.split(st.state_sep)[-1]
        data = await state.get_data()
        data_field_dict = data[self.config.data_field]
        data_field_dict[field_name] = message.text
        await state.update_data(
            {self.config.data_field: data_field_dict}
        )

    async def start(
        self, callback: CallbackQuery, state: FSMContext, lang: str
    ):
        state_handler = f'{self.config.router_state.state}:start'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        data = await state.get_data()

        await callback.answer()
        await state.update_data(
            {
                self.config.data_field: {
                    'company_uuid': data['company_uuid']
                }
            }
        )

        terminology_lang = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)

        core_buttons = await core_term_lang.buttons.get_dict_with(
            *self.config.states_group.core_buttons)

        keyboard = await create_simply_inline_kb(
            core_buttons,
            1
        )
        await callback.message.answer(
            text=terminology_lang.terms.start_create,
            reply_markup=keyboard
        )
        await state.set_state(self.config.router_state)

    async def done(
        self, message: Message, state: FSMContext, lang: str
    ):
        state_handler = f'{self.config.router_state.state}:done'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        await self.update_data(message=message, state=state)

        if await st.is_debag():
            data = await state.get_data()
            self.config.logger.info(f'{state_handler} {data=}')

        terminology_lang = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)

        core_buttons = await core_term_lang.buttons.get_dict_with(
            *self.config.states_group.core_buttons)

        keyboard = await create_simply_inline_kb(
            core_buttons,
            1
        )
        await message.answer(
            text=terminology_lang.terms.done,
            reply_markup=keyboard
        )
        await state.set_state(self.config.next_state)

    async def error(
        self, message: Message, lang: str
    ):
        state_handler = f'{self.config.router_state.state}:error'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        terminology_lang = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)

        core_buttons = await core_term_lang.buttons.get_dict_with(
            *self.config.states_group.core_buttons)

        keyboard = await create_simply_inline_kb(
            core_buttons,
            1
        )
        await message.answer(
            text=terminology_lang.terms.error,
            reply_markup=keyboard
        )


class CreateFieldStr(CreateField):
    def __init__(
        self,
        config: CreateConfig,
        max_lengh: int,
    ):
        self.config = config
        self.max_lengh = max_lengh
        self._register_handlers()

    def _register_mutable_handlers(self):
        self.config.router.message(
            StateFilter(self.config.router_state),
            F.text.len() <= self.max_lengh
        )(self.done)
