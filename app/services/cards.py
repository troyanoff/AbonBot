import logging

from functools import lru_cache

from services.api import get_api_service
from services.base import BaseService
from schemas.representations import (
    CardReprSchema,
    CardListSchema,
)
from schemas.utils import DoneSchema, FailSchema, ExceptSchema
from pprint import pformat


logger = logging.getLogger(__name__)


class CardService(BaseService):
    base_path: str = 'cards/'
    cache_prefix: str = 'cards'
    item_schema = CardReprSchema
    list_schema = CardListSchema

    async def archive(self, uuid: str):
        params = {
            'uuid': uuid
        }
        result = await self.api.delete(
            path=self.base_path + 'archive',
            params=params
        )
        if isinstance(result, (FailSchema, ExceptSchema)):
            logger.error(
                f'Error: {pformat(result.model_dump())}')
            return FailSchema()
        return DoneSchema()


@lru_cache()
def get_card_service() -> CardService:
    api = get_api_service()
    return CardService(api)
