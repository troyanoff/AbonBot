
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, Message
)
from aiogram.utils.keyboard import InlineKeyboardMarkup
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
        need_last_buttons: bool = False,
        last_buttons: tuple = None,
        last_term=None,
        next_state: State | tuple = None,
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

    async def done_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        terminology_lang = getattr(self.config.term, lang)
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

    async def error_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        core_term_lang: core_Lang = getattr(core_term, lang)
        if self.config.need_last_buttons:
            last_term_lang: core_Lang = getattr(self.config.last_term, lang)
            buttons = await last_term_lang.buttons.get_dict_with(
                *self.config.last_buttons
            )
            core_buttons = await core_term_lang.buttons.get_dict_with(
                *self.config.states_group.core_buttons)
            buttons.update(core_buttons)
        else:
            buttons = await core_term_lang.buttons.get_dict_with(
                *self.config.states_group.core_buttons)

        keyboard = await create_simply_inline_kb(
            buttons,
            1
        )

        return keyboard

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

        keyboard = await self.done_keyboard(lang)

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

        keyboard = await self.error_keyboard(lang)

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


class CreateFieldBool(CreateField):
    def __init__(
        self,
        config: CreateConfig,
        buttons: tuple[tuple, tuple]
    ):
        self.config = config
        self.buttons = buttons
        self.callbacks = ('yes', 'no')
        self.next_state_dict = {callback: state for callback, state in zip(
            self.callbacks, self.config.next_state)}
        self._register_handlers()

    def _register_mutable_handlers(self):
        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.in_(self.callbacks)
        )(self.done)

    async def update_data(self, callback: CallbackQuery, state: FSMContext):
        field_name = self.config.router_state.state.split(st.state_sep)[-1]
        data = await state.get_data()
        data_field_dict = data[self.config.data_field]
        data_field_dict[field_name] = callback.data == 'yes'
        await state.update_data(
            {self.config.data_field: data_field_dict}
        )

    async def done_keyboard(
        self, lang: str, result: bool
    ) -> InlineKeyboardMarkup:
        terminology_lang = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)

        buttons = await terminology_lang.buttons.get_dict_with(
            *(self.buttons[0] if result else self.buttons[1])
        )
        core_buttons = await core_term_lang.buttons.get_dict_with(
            *self.config.states_group.core_buttons)
        buttons.update(core_buttons)

        keyboard = await create_simply_inline_kb(
            buttons,
            1
        )

        return keyboard

    async def done(
        self, callback: CallbackQuery, state: FSMContext, lang: str
    ):
        state_handler = f'{self.config.router_state.state}:done'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        result = callback.data == 'yes'

        await self.update_data(callback=callback, state=state)

        if await st.is_debag():
            data = await state.get_data()
            self.config.logger.info(f'{state_handler} {data=}')

        terminology_lang = getattr(self.config.term, lang)

        keyboard = await self.done_keyboard(lang, result)

        await callback.message.answer(
            text=(
                terminology_lang.terms.done_yes if result
                else terminology_lang.terms.done_no
            ),
            reply_markup=keyboard
        )
        await state.set_state(self.next_state_dict[callback.data])


class CreateFieldInt(CreateField):
    def __init__(
        self,
        config: CreateConfig,
        interval: tuple[int, int],  # inclusive (<=, <=)
    ):
        self.config = config
        self.interval = interval
        self._register_handlers()

    def _register_mutable_handlers(self):
        self.config.router.message(
            StateFilter(self.config.router_state),
            F.text.regexp(r'^-?\d+$'),
            lambda msg: self.interval[0] <= int(msg.text) <= self.interval[1]
        )(self.done)

    async def update_data(self, message: Message, state: FSMContext):
        field_name = self.config.router_state.state.split(st.state_sep)[-1]
        data = await state.get_data()
        data_field_dict = data[self.config.data_field]
        data_field_dict[field_name] = int(message.text)
        await state.update_data(
            {self.config.data_field: data_field_dict}
        )
