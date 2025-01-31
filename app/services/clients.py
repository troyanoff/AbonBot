import aiohttp

from functools import lru_cache

from services.api import APIService, get_api_service
from services.base import BaseService
from schemas.clients import ClientCreateSchema


class ClientService(BaseService):
    base_path: str = 'clients/'

    def __init__(self, api: APIService):
        self.api = api

    async def create(self, client: ClientCreateSchema):
        data = client.model_dump_json()
        response = await self.api.post(
            path='', data=data
        )
        print(response)
        

@lru_cache()
def get_client_service() -> ClientService:
    api = get_api_service()
    return ClientService(api)


