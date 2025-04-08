import logging

from functools import lru_cache

from services.api import get_api_service
from services.base import BaseService
from schemas.representations import (
    LocationReprSchema,
    LocationListSchema
)


logger = logging.getLogger(__name__)


class LocationService(BaseService):
    base_path: str = 'locations/'
    cache_prefix: str = 'locations'
    item_schema = LocationReprSchema
    list_schema = LocationListSchema


@lru_cache()
def get_location_service() -> LocationService:
    api = get_api_service()
    return LocationService(api)
