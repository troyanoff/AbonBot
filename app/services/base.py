import logging

from pydantic import BaseModel

from core.config import settings as st
from services.api import APIService
from schemas.utils import FailSchema, ExceptSchema
from pprint import pformat


logger = logging.getLogger(__name__)


class BaseService:
    base_path: str
    cache_prefix: str
    item_schema: BaseModel
    list_schema: BaseModel

    def __init__(self, api: APIService):
        self.api = api

    async def _conversion(self, item: dict) -> BaseModel:
        result = self.item_schema(**item)
        return result

    async def list_conversion(self, items: dict) -> BaseModel:
        result = self.list_schema(**items)
        return result

    async def create(self, item: BaseModel):
        data = item.model_dump_json()
        response = await self.api.post(
            path=self.base_path, data=data
        )

        if await st.is_debag():
            logger.info(f'{self.base_path} create {response=}')

        if isinstance(response, (FailSchema, ExceptSchema)):
            return FailSchema()
        return response

    async def update(self, update_schema: BaseModel):
        json_data = update_schema.model_dump_json(exclude_unset=True)
        response = await self.api.patch(
            path=self.base_path, data=json_data
        )
        if isinstance(response, (FailSchema, ExceptSchema)):
            logger.error(
                f'Error: {pformat(response.model_dump())}')
            return FailSchema()
        return response

    async def get(self, **kwargs) -> BaseModel:
        result = await self.api.get(
            path=self.base_path + 'get',
            params=kwargs
        )
        if isinstance(result, (FailSchema, ExceptSchema)):
            logger.error(
                f'Error: {pformat(result.model_dump())}')
            return FailSchema()
        data = result.response.data
        item = await self._conversion(data)
        return item

    async def get_list(
        self,
        limit: int = st.default_limit_keyboard_page,
        offset: int = 0,
        **kwargs
    ) -> BaseModel:
        params = {
            'limit': limit,
            'offset': offset
        }
        params.update(kwargs)
        result = await self.api.get(
            path=self.base_path,
            params=params
        )
        if isinstance(result, (FailSchema, ExceptSchema)):
            logger.error(
                f'Error: {pformat(result.model_dump())}')
            return FailSchema()
        data = result.response.data
        items = await self.list_conversion(data)
        return items
