
from aiogram.utils.keyboard import InlineKeyboardMarkup
from dataclasses import dataclass, field
from pydantic import BaseModel

from handlers.base import LastMessage, BaseConfig, BaseHandler, Data, RequestTG
from services.base import BaseService


@dataclass
class ManageConfig(BaseConfig):
    format_caption: dict = field(default_factory=lambda: {})


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

    async def _create_caption(self, data: Data, item: BaseModel):
        content = {
            k: getattr(item, v) for k, v in self.config.format_caption.items()}
        result = data.term.local.terms.manage_content.format(**content)
        return result

    async def _choise_media(self, data: Data, item: BaseModel) -> str:
        if getattr(item, 'photo_id', None):
            return item.photo_id
        return getattr(data.term.core.photos, self.config.stug_photo_name)

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
