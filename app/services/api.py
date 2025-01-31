import aiohttp

from functools import lru_cache

from core.config import settings
from schemas.api import Login, ResponseShema
from services.storage import RedisService, get_redis_service
from utils.decorators import safe_exec_api


class APIService:
    base_url: str = settings.api_host + settings.api_version
    
    def __init__(self, storage: RedisService):
        self.storage = storage

    async def _get_token(self) -> str:
        """Get bearer token."""
        headers = {
            'Content-Type': 'application/json'
        }
        params = {}
        url = self.base_url + 'auth/login'
        data = Login(
            login=settings.api_login,
            password=settings.api_password
        ).model_dump_json()
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                url=url,
                headers=headers,
                params=params,
                data=data
            ) as response:
                status = response.status
                response = await response.json()
                print(status)
                print(response)
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        await self.storage.set(
            'access_token', access_token, settings.access_token_ttl)
        await self.storage.set(
            'refresh_token', refresh_token, settings.refresh_token_ttl)
        return access_token


    async def _auth_handler(self) -> str:
        """Create or get auth token."""
        token_by_storage = await self.storage.get('access_token')
        if token_by_storage:
            return f'Bearer {token_by_storage}'
        token_by_api = await self._get_token()
        return f'Bearer {token_by_api}'

    async def _get_headers(self) -> dict:
        result = {
            'Content-Type': 'application/json',
            'Authorization': await self._auth_handler()
        }
        return result

    @safe_exec_api
    async def get(
        self,
        path: str,
        params: dict = {},
        data: str = None,
        timeout: int = 20
    ) -> ResponseShema:
        """GET request."""
        url = self.base_url + path
        headers = await self._get_headers()
        timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                url=url,
                headers=headers,
                params=params,
                data=data
            ) as response:
                status = response.status
                response = await response.json()
        return ResponseShema(status=status, data=response)

    @safe_exec_api
    async def post(
        self,
        path: str,
        params: dict = {},
        data: str = None,
        timeout: int = 20
    ) -> ResponseShema:
        """POST request."""
        url = self.base_url + path
        headers = await self._get_headers()
        timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                url=url,
                headers=headers,
                params=params,
                data=data
            ) as response:
                status = response.status
                response = await response.json()
        return ResponseShema(status=status, data=response)


@lru_cache()
def get_api_service() -> APIService:
    storage = get_redis_service()
    return APIService(storage)
