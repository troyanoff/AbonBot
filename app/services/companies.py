import logging

from functools import lru_cache

from services.api import get_api_service
from services.base import BaseService
from schemas.representations import (
    CompanyReprSchema,
    CompanyListSchema,
)


logger = logging.getLogger(__name__)


class CompanyService(BaseService):
    base_path: str = 'companies/'
    cache_prefix: str = 'companies'
    item_schema = CompanyReprSchema
    list_schema = CompanyListSchema


@lru_cache()
def get_company_service() -> CompanyService:
    api = get_api_service()
    return CompanyService(api)
