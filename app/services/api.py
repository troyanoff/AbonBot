import aiohttp

from functools import lru_cache

from core.config import settings
from schemas.api import Login, ResponseShema
from services.cache import Cache, get_cache_service
from utils.decorators import safe_exec_api


class APIService:
    base_url: str = settings.api_host + settings.api_version
    cache_prefix: str = 'api_service'
    
    def __init__(self, cache: Cache):
        self.cache = cache

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
        await self.cache.set(
            self.cache_prefix,
            'access_token',
            access_token,
            settings.access_token_ttl
        )
        await self.cache.set(
            self.cache_prefix,
            'refresh_token',
            refresh_token,
            settings.refresh_token_ttl)
        return access_token


    async def _auth_handler(self) -> str:
        """Create or get auth token."""
        token_by_cache = await self.cache.get(
            self.cache_prefix, 'access_token')
        if token_by_cache:
            return f'Bearer {token_by_cache}'
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

    @safe_exec_api
    async def put(
        self,
        path: str,
        params: dict = {},
        data: str = None,
        timeout: int = 20
    ) -> ResponseShema:
        """PUT request."""
        url = self.base_url + path
        headers = await self._get_headers()
        timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.put(
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
    cache = get_cache_service()
    return APIService(cache)
