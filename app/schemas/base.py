import orjson

from enum import Enum
from pydantic import BaseModel
from uuid import UUID


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class MyBaseModel(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        populate_by_name = True


class MyBaseModelUUID(BaseModel):
    uuid: str | UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        populate_by_name = True


class SexEnum(str, Enum):
    m = 'm'
    f = 'f'
