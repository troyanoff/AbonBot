import logging
import orjson

from aiohttp.web import HTTPOk
from pprint import pformat
from functools import lru_cache

from services.api import APIService, get_api_service
from services.base import BaseService
from services.cache import Cache, get_cache_service
from schemas.clients import ClientCreateSchema
from schemas.representations import (
    ClientReprSchema,
    CompanyMinReprSchema,
    SubscriptionMinReprSchema,
    RecordMinReprSchema
)
from schemas.utils import ExceptSchema, DoneSchema, FailSchema


logger = logging.getLogger(__name__)


class ClientService(BaseService):
    base_path: str = 'clients/'
    cache_prefix: str = 'clients'

    def __init__(self, api: APIService, cache: Cache):
        self.api = api
        self.cache = cache

    async def _conversion(self, item: dict) -> ClientReprSchema:
        # companies = item['companies']
        # subscriptions = item['subscriptions']
        # records = item['records']
        # item['companies'] = [CompanyMinReprSchema(**i) for i in companies]
        # item['subscriptions'] = [
        #     SubscriptionMinReprSchema(**i) for i in subscriptions]
        # item['records'] = [RecordMinReprSchema(**i) for i in records]
        result = ClientReprSchema(**item)
        return result

    # async def del_client_cache(self, tg_id: int):
    #     await self.cache.delete(self.cache_prefix, tg_id)

    async def create(self, client: ClientCreateSchema):
        data = client.model_dump_json()
        response = await self.api.post(
            path=self.base_path, data=data
        )
        logger.info(f'client_create {response=}')
        if isinstance(response, (FailSchema, ExceptSchema)):
            return FailSchema()
        return response

    async def update(self, tg_id: int, update_data: dict):
        data = orjson.dumps(update_data)
        response = await self.api.patch(
            path=self.base_path, data=data
        )
        if isinstance(response, (FailSchema, ExceptSchema)):
            logger.error(
                f'Возникла ошибка: {pformat(response.model_dump())}')
            return False
        await self.cache.delete(self.cache_prefix, tg_id)
        return True

    async def get(self, tg_id: int) -> ClientReprSchema:
        logger.info('Проверяем кэш')
        data = await self.cache.get(self.cache_prefix, tg_id)
        if not data:
            logger.info('В кэше объекта не оказалось')
            params = {
                'tg_id': tg_id
            }
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
            logger.info('Кладем объект в кэш')
            await self.cache.set(self.cache_prefix, tg_id, data)
        item = await self._conversion(data)
        return item


@lru_cache()
def get_client_service() -> ClientService:
    api = get_api_service()
    cache = get_cache_service()
    return ClientService(api, cache)
