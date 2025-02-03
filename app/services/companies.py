import logging
import orjson

from aiohttp.web import HTTPOk
from functools import lru_cache

from services.api import APIService, get_api_service
from services.base import BaseService
from services.cache import Cache, get_cache_service
from schemas.companies import CompanyCreateSchema
from schemas.representations import (
    ClientReprSchema,
    CompanyReprSchema,
    SubscriptionMinReprSchema,
    RecordMinReprSchema
)


loger = logging.getLogger(__name__)


class CompanyService(BaseService):
    base_path: str = 'companies/'
    cache_prefix: str = 'companies'

    def __init__(self, api: APIService, cache: Cache):
        self.api = api
        self.cache = cache

    async def _conversion(self, item: dict) -> CompanyReprSchema:
        result = CompanyReprSchema(**item)
        return result

    async def del_company_cache(self, creator_uuid: str):
        await self.cache.delete(self.cache_prefix, creator_uuid)

    async def create(self, company: CompanyCreateSchema):
        data = company.model_dump_json()
        response = await self.api.post(
            path=self.base_path, data=data
        )
        if response.status != HTTPOk.status_code:
            return None
        await self.cache.delete(self.cache_prefix, company.creator_uuid)
        return response

    async def update(self, creator_uuid: str, update_data: dict):
        data = orjson.dumps(update_data)
        response = await self.api.put(
            path=self.base_path, data=data
        )
        if response.status != HTTPOk.status_code:
            return None
        await self.cache.delete(self.cache_prefix, creator_uuid)
        return response

    async def get(self, tg_id: int) -> ClientReprSchema:
        data = await self.cache.get(self.cache_prefix, tg_id)
        if not data:
            params = {
                'tg_id': tg_id
            }
            result = await self.api.get(
                path=self.base_path + 'get',
                params=params
            )
            if result.status != HTTPOk.status_code:
                return None
            data = result.data
            await self.cache.set(self.cache_prefix, tg_id, data)
        item = await self._conversion(data)
        return item

    async def get_list(self, client_uuid: str) -> list[CompanyReprSchema]:
        data = await self.cache.get(self.cache_prefix, client_uuid)
        if not data:
            params = {
                'creator_uuid': client_uuid
            }
            result = await self.api.get(
                path=self.base_path,
                params=params
            )
            if result.status != HTTPOk.status_code:
                return None
            data = result.data
            if data:
                await self.cache.set(self.cache_prefix, client_uuid, data)
        items = [await self._conversion(i) for i in data]
        return items
        

@lru_cache()
def get_company_service() -> CompanyService:
    api = get_api_service()
    cache = get_cache_service()
    return CompanyService(api, cache)


