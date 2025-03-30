import aiohttp
import logging

from functools import lru_cache

from core.config import settings
from schemas.api import Login, ResponseShema
from schemas.utils import DoneSchema, FailSchema
from services.cache import Cache, get_cache_service
from utils.decorators import safe_exec_api


logger = logging.getLogger(__name__)


class APIService:
    base_url: str = settings.api_host + settings.api_version
    cache_prefix: str = 'api_service'

    def __init__(self, cache: Cache):
        self.cache = cache

    async def _login(self) -> str:
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
                # status = response.status
                response = await response.json()
                logger.info(f'{response=}')
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

    async def _refresh(self, refresh_token: str) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {refresh_token}'
        }
        url = self.base_url + 'auth/refresh'
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                url=url,
                headers=headers
            ) as response:
                # status = response.status
                response = await response.json()
                logger.info(f'{response=}')
        access_token = response['access_token']
        await self.cache.set(
            self.cache_prefix,
            'access_token',
            access_token,
            settings.access_token_ttl
        )
        return access_token

    async def _auth_handler(self) -> str:
        """Create or get auth token."""
        token_by_cache_exist = await self.cache.exists(
            self.cache_prefix, 'access_token')
        if token_by_cache_exist:
            token_by_cache = await self.cache.get(
                self.cache_prefix, 'access_token'
            )
            return f'Bearer {token_by_cache}'
        refresh_by_cache_exist = await self.cache.exists(
            self.cache_prefix, 'refresh_token'
        )
        if refresh_by_cache_exist:
            refresh_by_cache = await self.cache.get(
                self.cache_prefix, 'refresh_token'
            )
            access_token = await self._refresh(refresh_by_cache)
            return f'Bearer {access_token}'
        token_by_api = await self._login()
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
    ) -> DoneSchema | FailSchema:
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
                try:
                    response = await response.json()
                except Exception:
                    response = await response.text()
        if 200 <= status < 300:
            return DoneSchema(
                response=ResponseShema(status=status, data=response)
            )
        return FailSchema(
            response=ResponseShema(status=status, data=response)
        )

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
                try:
                    response = await response.json()
                except Exception:
                    response = await response.text()
        if 200 <= status < 300:
            return DoneSchema(
                response=ResponseShema(status=status, data=response)
            )
        return FailSchema(
            response=ResponseShema(status=status, data=response)
        )

    @safe_exec_api
    async def patch(
        self,
        path: str,
        params: dict = {},
        data: str = None,
        timeout: int = 20
    ) -> ResponseShema:
        """PATCH request."""
        url = self.base_url + path
        headers = await self._get_headers()
        timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.patch(
                url=url,
                headers=headers,
                params=params,
                data=data
            ) as response:
                status = response.status
                try:
                    response = await response.json()
                except Exception:
                    response = await response.text()
        if 200 <= status < 300:
            return DoneSchema(
                response=ResponseShema(status=status, data=response)
            )
        return FailSchema(
            response=ResponseShema(status=status, data=response)
        )

    @safe_exec_api
    async def delete(
        self,
        path: str,
        params: dict = {},
        timeout: int = 20
    ) -> ResponseShema:
        """DELETE request."""
        url = self.base_url + path
        headers = await self._get_headers()
        timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.delete(
                url=url,
                headers=headers,
                params=params
            ) as response:
                status = response.status
                try:
                    response = await response.json()
                except Exception:
                    response = await response.text()
        if 200 <= status < 300:
            return DoneSchema(
                response=ResponseShema(status=status, data=response)
            )
        return FailSchema(
            response=ResponseShema(status=status, data=response)
        )


@lru_cache()
def get_api_service() -> APIService:
    cache = get_cache_service()
    return APIService(cache)
