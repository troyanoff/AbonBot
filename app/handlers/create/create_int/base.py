from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message
)

from core.config import settings as st
from handlers.create.base import CreateConfig, CreateField


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
