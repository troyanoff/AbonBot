from aiohttp.web import HTTPOk
from functools import lru_cache

from services.api import APIService, get_api_service
from services.base import BaseService
from schemas.clients import ClientCreateSchema
from schemas.representations import (
    ClientReprSchema,
    CompanyMinReprSchema,
    SubscriptionMinReprSchema,
    RecordMinReprSchema
)


class ClientService(BaseService):
    base_path: str = 'clients/'

    def __init__(self, api: APIService):
        self.api = api

    async def _conversion(self, item: dict) -> ClientReprSchema:
        companies = item['companies']
        subscriptions = item['subscriptions']
        records = item['records']
        item['companies'] = [CompanyMinReprSchema(**i) for i in companies]
        item['subscriptions'] = [
            SubscriptionMinReprSchema(**i) for i in subscriptions]
        item['records'] = [RecordMinReprSchema(**i) for i in records]
        result = ClientReprSchema(**item)
        return result

    async def create(self, client: ClientCreateSchema):
        data = client.model_dump_json()
        response = await self.api.post(
            path=self.base_path, data=data
        )
        print(response)

    async def get(self, tg_id: int) -> ClientReprSchema:
        params = {
            'tg_id': tg_id
        }
        result = await self.api.get(
            path=self.base_path + 'get',
            params=params
        )
        if result.status != HTTPOk.status_code:
            return None
        item = await self._conversion(result.data)
        return item
        

@lru_cache()
def get_client_service() -> ClientService:
    api = get_api_service()
    return ClientService(api)


