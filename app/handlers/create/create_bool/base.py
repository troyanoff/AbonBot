from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, Message
)
from aiogram.utils.keyboard import InlineKeyboardMarkup

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from handlers.create.base import CreateConfig, CreateField
from keyboards.inline.base import create_simply_inline_kb


class CreateFieldBool(CreateField):
    def __init__(
        self,
        config: CreateConfig,
        buttons: tuple[tuple, tuple],
        end_caller_callback: str = None
    ):
        self.config = config
        self.buttons = buttons
        self.end_caller_callback = end_caller_callback
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

    async def done_end(
        self,
        update: Message | CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        result = update.data == 'yes'

        terminology_lang = getattr(self.config.term, lang)

        keyboard = await self.done_keyboard(lang, result)

        await update.message.answer(
            text=(
                terminology_lang.terms.done_yes if result
                else terminology_lang.terms.done_no
            ),
            reply_markup=keyboard
        )
        await state.set_state(self.next_state_dict[update.data])

    async def done(
        self, callback: CallbackQuery, state: FSMContext, lang: str
    ):
        state_handler = f'{self.config.router_state.state}:done'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        await self.update_data(callback=callback, state=state)
        result = callback.data == 'yes'

        if await st.is_debag():
            data = await state.get_data()
            self.config.logger.info(f'{state_handler} {data=}')

        done_func = self.done_end

        if (self.config.end_caller
                and callback.data == self.end_caller_callback
                and not result):
            done_func = self.config.end_caller

        await done_func(callback, state=state, lang=lang)
