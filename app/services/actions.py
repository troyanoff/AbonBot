import logging

from functools import lru_cache

from services.api import get_api_service
from services.base import BaseService
from schemas.representations import (
    ActionReprSchema,
    ActionListSchema,
)
from schemas.utils import DoneSchema, FailSchema, ExceptSchema
from pprint import pformat


logger = logging.getLogger(__name__)


class ActionService(BaseService):
    base_path: str = 'actions/'
    cache_prefix: str = 'actions'
    item_schema = ActionReprSchema
    list_schema = ActionListSchema

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
def get_action_service() -> ActionService:
    api = get_api_service()
    return ActionService(api)
