from aiogram.fsm.state import State
from dataclasses import dataclass
from pydantic import BaseModel
from types import CoroutineType

from handlers.base import BaseConfig, Data, RequestTG, BaseHandler
from handlers.create.base import CreateField
from services.base import BaseService


@dataclass
class RememberConfig:
    service_caller: BaseService
    generated_field: str
    schema: BaseModel
    queue: list[CreateField]
    manage_caller: str | CoroutineType


class Remember(BaseHandler):
    index_name: str = 'now_index'

    def __init__(self, config: RememberConfig):
        self.config = config
        self.del_after = (self.index_name, self.config.generated_field)
        self._queue_notification()

    async def get_state_key(self, request_tg: RequestTG, key: str):
        state_data = await request_tg.state.get_data()
        return state_data.get(key)

    def _queue_notification(self):
        for elem in self.config.queue:
            elem.handler = self

    async def next_state(self, request_tg: RequestTG):
        now_index = await self.get_state_key(request_tg, self.index_name)
        new_index = 0 if now_index is None else now_index + 1
        if new_index == len(self.config.queue):
            await self.end(request_tg)
            return
        await request_tg.state.update_data(now_index=new_index)
        await request_tg.state.set_state(
            self.config.queue[new_index].config.router_state)
        await self.config.queue[new_index](request_tg=request_tg)

    async def __call__(self, request_tg: RequestTG):
        await request_tg.state.update_data({self.config.generated_field: {
            'tg_id': request_tg.update.from_user.id
        }})
        await self.next_state(request_tg)

    async def end(self, request_tg: RequestTG):
        pass


class RememberCreate(Remember):
    async def end(self, request_tg: RequestTG):
        service: BaseService = self.config.service_caller()
        state_data = await request_tg.state.get_data()
        generated_data = state_data[self.config.generated_field]
        generated_schema = self.config.schema.model_validate(generated_data)
        result = await service.create(
            generated_schema
        )
        # if await self.bad_response(data, result):
        #     return

        caller = await self.choise_caller(self.config.manage_caller)
        await caller(request_tg,
                     uuid=result.response.data['item']['uuid'])


class RememberUpdate(Remember):
    async def end(self, data: Data):
        service: BaseService = self.config.service_caller()
        state_data = await data.request.state.get_data()
        generated_data = state_data[self.config.generated_field]
        generated_schema = self.config.schema.model_validate(generated_data)
        result = await service.update(
            generated_schema
        )
        if await self.bad_response(data, result):
            return

        caller = await self.choise_caller(self.config.manage_caller)
        await caller(data.request, uuid=result.response.data['item']['uuid'])
