
from aiogram.utils.keyboard import InlineKeyboardMarkup
from enum import Enum
from dataclasses import dataclass, field
from pydantic import BaseModel

from handlers.base import LastMessage, BaseConfig, BaseHandler, Data, RequestTG
from services.base import BaseService


@dataclass
class ManageConfig(BaseConfig):
    format_caption: dict = field(default_factory=lambda: {})
    set_item_data: dict = field(default_factory=lambda: {})


class ManageBase(BaseHandler):

    def __init__(
        self,
        config: ManageConfig
    ):
        self.config = config
        self._register_handlers()

    def _register_handlers(self):
        super()._register_handlers()

    async def _create_keyboard(self, data: Data) -> InlineKeyboardMarkup:
        keyboard = await self.create_simply_kb(data)
        return keyboard

    async def get_item_field(
            self, data: Data, field_name: str, item: BaseModel):
        field_value = await self._getattr_model(item, field_name)
        if isinstance(field_value, Enum):
            core_value = getattr(data.term.core.terms, field_value.name, None)
            if core_value:
                field_value = core_value
        return field_value

    async def _create_caption(self, data: Data, item: BaseModel):
        content = {
            k: await self.get_item_field(data, v, item)
            for k, v in self.config.format_caption.items()}
        result = data.term.local.terms.manage_content.format(**content)
        return result

    async def _choise_media(self, data: Data, item: BaseModel) -> str:
        if getattr(item, 'photo_id', None):
            return item.photo_id
        return getattr(data.term.core.photos, self.config.stug_photo_name)

    async def set_item_data(self, data: Data, item: BaseModel):
        if not self.config.set_item_data:
            return
        update_data = {}
        for k, v in self.config.set_item_data.items():
            update_data[k] = await self._getattr_model(item, v)
        await data.request.state.update_data(update_data)

    async def __call__(
        self,
        request_tg: RequestTG
    ):
        data: Data = self._update_to_request_data(
            'call', request_tg
        )
        await self.next_state_group(data)

        uuid = await self.get_state_key(
            data, f'{self.config.item_prefix}_uuid')

        service: BaseService = self.config.service_caller()
        item = await service.get(uuid=uuid)
        if await self.bad_response(data, item):
            return

        await self.set_item_data(data, item)

        text = await self._create_caption(data, item)
        photo = await self._choise_media(data, item)
        keyboard = await self._create_keyboard(data)
        state_data = await data.request.state.get_data()
        last_message = LastMessage(
            state=self.config.router_state.state,
            text=text,
            photo=photo,
            keyboard=keyboard,
            state_instance=state_data
        )
        await self.remember_answer(data, last_message)
        await self.answer(data, last_message)

    async def archive(
        self,
        request_tg: RequestTG
    ):
        data = self._update_to_request_data('archive', request_tg)
        uuid = await self.get_state_key(
            data, f'{self.config.item_prefix}_uuid')

        service = self.config.service_caller()
        result = await service.archive(uuid)
        if await self.bad_response(data, result):
            return
        await data.request.update.answer(data.term.local.terms.archived)
        await self.to_last_state(
            callback=data.request.update,
            lang=data.request.lang,
            state=data.request.state
        )
