from aiogram import F
from aiogram.filters import StateFilter

from handlers.create.base import CreateConfig, CreateField


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
