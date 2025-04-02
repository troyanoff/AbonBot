import logging

from functools import lru_cache

from services.api import get_api_service
from services.base import BaseService
from schemas.representations import (
    ClientReprSchema,
    ClientListSchema,
)


logger = logging.getLogger(__name__)


class ClientService(BaseService):
    base_path: str = 'clients/'
    cache_prefix: str = 'clients'
    item_schema = ClientReprSchema
    list_schema = ClientListSchema


@lru_cache()
def get_client_service() -> ClientService:
    api = get_api_service()
    return ClientService(api)
