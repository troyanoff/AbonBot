import logging

from functools import lru_cache

from core.config import settings as st
from services.api import APIService, get_api_service
from services.base import BaseService
from services.cache import Cache, get_cache_service
from schemas.events import (
    EventCreateSchema, EventUpdateSchema
)
from schemas.representations import (
    ClientReprSchema,
    EventReprSchema,
    EventListSchema,
)
from schemas.utils import DoneSchema, FailSchema, ExceptSchema
from pprint import pformat


logger = logging.getLogger(__name__)


class EventService(BaseService):
    base_path: str = 'events/'
    cache_prefix: str = 'events'

    def __init__(self, api: APIService, cache: Cache):
        self.api = api
        self.cache = cache

    async def _conversion(self, item: dict) -> EventReprSchema:
        result = EventReprSchema(**item)
        return result

    async def list_conversion(self, items: dict) -> EventListSchema:
        result = EventListSchema(**items)
        return result

    async def create(self, event: EventCreateSchema):
        data = event.model_dump_json()
        response = await self.api.post(
            path=self.base_path, data=data
        )
        logger.info(f'event create {response=}')
        if isinstance(response, (FailSchema, ExceptSchema)):
            return FailSchema()
        return response

    async def update(self, data: EventUpdateSchema):
        json_data = data.model_dump_json(exclude_unset=True)
        response = await self.api.patch(
            path=self.base_path, data=json_data
        )
        if isinstance(response, (FailSchema, ExceptSchema)):
            logger.error(
                f'Error: {pformat(response.model_dump())}')
            return FailSchema()
        await self.cache.delete(self.cache_prefix, data.uuid)
        return DoneSchema()

    async def get(self, uuid: str = None, **kwargs) -> ClientReprSchema:
        data = await self.cache.get(self.cache_prefix, uuid)
        if not data:
            params = {}
            if uuid:
                params['uuid'] = uuid
            params.update(kwargs)
            result = await self.api.get(
                path=self.base_path + 'get',
                params=params
            )
            if isinstance(result, (FailSchema, ExceptSchema)):
                if isinstance(result, FailSchema):
                    return result
                logger.error(
                    f'Возникла ошибка: {pformat(result.model_dump())}')
                return FailSchema()
            data = result.response.data
            logger.info('Set data to cache')
            await self.cache.set(self.cache_prefix, uuid, data)
        item = await self._conversion(data)
        return item

    async def get_list(
        self,
        company_uuid: str = None,
        limit: int = st.default_limit_keyboard_page,
        offset: int = 0,
        **kwargs
    ) -> EventListSchema:
        data = await self.cache.get(
            self.cache_prefix, f'{company_uuid=}:{limit=}:{offset=}:{kwargs=}'
        )
        if not data:
            params = {
                'limit': limit,
                'offset': offset
            }
            if company_uuid:
                params['company_uuid'] = company_uuid
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
            logger.info('Set data to cache')
            await self.cache.set(
                self.cache_prefix,
                f'{company_uuid=}:{limit=}:{offset=}:{kwargs=}',
                data
            )
        items = await self.list_conversion(data)
        return items

    async def archive(self, uuid: str):
        params = {
            'uuid': uuid
        }
        result = await self.api.delete(
            path=self.base_path + 'archive',
            params=params
        )
        if isinstance(result, (FailSchema, ExceptSchema)):
            logger.error(
                f'Error: {pformat(result.model_dump())}')
            return FailSchema()
        return DoneSchema()


@lru_cache()
def get_event_service() -> EventService:
    api = get_api_service()
    cache = get_cache_service()
    return EventService(api, cache)
