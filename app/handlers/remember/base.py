from aiogram.types import Message, CallbackQuery
from dataclasses import dataclass
from importlib import import_module
from pydantic import BaseModel
from types import CoroutineType

from core.terminology import terminology as core_term, Lang as core_Lang
from handlers.base import RequestTG
from handlers.create.base import CreateField
from schemas.base import RememberTypeEnum
from schemas.utils import DoneSchema, FailSchema
from services.base import BaseService


@dataclass
class RememberConfig:
    remember_type: RememberTypeEnum
    item_prefix: str
    service_caller: BaseService
    generated_field: str
    schema: BaseModel
    queue: list[CreateField]
    manage_caller: str | CoroutineType
    exists_fields: tuple = (
        ('company_uuid', 'company_uuid'),
    )
    additional_end_func: CoroutineType = None


class Remember:
    index_name: str = 'now_index'

    def __init__(self, config: RememberConfig):
        self.config = config
        self.del_after = (self.index_name, self.config.generated_field)
        self._queue_notification()

    def _queue_notification(self):
        for elem in self.config.queue:
            elem.handler = self

    async def choise_caller(
        self, caller_entity: str | CoroutineType
    ) -> CoroutineType:
        if isinstance(caller_entity, CoroutineType):
            return caller_entity
        module_path, caller = caller_entity.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, caller)

    async def choise_message(self, request_tg: RequestTG) -> Message:
        if isinstance(request_tg.update, CallbackQuery):
            return request_tg.update.message
        return request_tg.update

    async def bad_response(
        self,
        request_tg: RequestTG,
        response: DoneSchema | FailSchema
    ) -> bool:
        if isinstance(response, FailSchema):
            core_lang: core_Lang = getattr(core_term, request_tg.lang)
            text = core_lang.terms.error
            photo = core_lang.photos.error
            keyboard = None
            msg = await self.choise_message(request_tg)
            await msg.answer_photo(
                photo=photo,
                caption=text,
                reply_markup=keyboard
            )
            await request_tg.state.clear()
            await request_tg.state.set_state('FSMDefault:default')
            return True

    async def get_state_key(self, request_tg: RequestTG, key: str):
        state_data = await request_tg.state.get_data()
        return state_data.get(key)

    async def next_state(self, request_tg: RequestTG):
        now_index = await self.get_state_key(request_tg, self.index_name)
        new_index = 0 if now_index is None else now_index + 1
        if new_index == len(self.config.queue):
            await self.end(request_tg)
            return
        await request_tg.state.update_data(now_index=new_index)
        await request_tg.state.set_state(
            self.config.queue[new_index].config.router_state)

        last_message_json = await self.get_state_key(
            request_tg, 'last_message')
        if not last_message_json:
            await request_tg.state.update_data(state_path=[])
            return
        state_path: list = await self.get_state_key(request_tg, 'state_path')
        state_path.append(last_message_json)
        await request_tg.state.update_data(state_path=state_path)

        await self.config.queue[new_index](request_tg=request_tg)

    async def create_start_fields(self, request_tg: RequestTG):
        state_data = await request_tg.state.get_data()
        start_fields = {}
        for key, key_exist in self.config.exists_fields:
            if key == 'tg_id':
                start_fields[key] = request_tg.update.from_user.id
            else:
                start_fields[key] = state_data[key_exist]

        await request_tg.state.update_data(
            {self.config.generated_field: start_fields}
        )

    async def remove_remember_keys(self, request_tg: RequestTG):
        state_data = await request_tg.state.get_data()
        for _field in self.del_after:
            del state_data[_field]
        await request_tg.state.set_data(state_data)

    async def __call__(self, request_tg: RequestTG):
        await self.create_start_fields(request_tg)
        await self.next_state(request_tg)

    async def end(self, request_tg: RequestTG):
        state_data = await request_tg.state.get_data()
        generated_data = state_data[self.config.generated_field]
        generated_schema = self.config.schema.model_validate(generated_data)

        service: BaseService = self.config.service_caller()

        if self.config.remember_type == RememberTypeEnum.create:
            result = await service.create(
                generated_schema
            )
        elif self.config.remember_type == RememberTypeEnum.update:
            result = await service.update(
                generated_schema
            )

        if await self.bad_response(request_tg, result):
            return

        await request_tg.state.update_data(
            {f'{self.config.item_prefix}_uuid':
                result.response.data['item']['uuid']}
        )

        if self.config.additional_end_func:
            await self.config.additional_end_func(request_tg)

        await self.remove_remember_keys(request_tg)

        caller = await self.choise_caller(self.config.manage_caller)
        await caller(request_tg)
