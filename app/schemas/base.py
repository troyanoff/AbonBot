import orjson

from datetime import datetime
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


class MyBaseModelRepr(BaseModel):
    uuid: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        populate_by_name = True


class BaseReprListSchema(BaseModel):
    items: list[BaseModel]
    total_count: int

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        populate_by_name = True


class MinItemSchema(BaseModel):
    uuid: UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        populate_by_name = True


class SexEnum(str, Enum):
    m = 'm'
    f = 'f'


class ClientRoleEnum(str, Enum):
    superclient = 'superclient'
    staff = 'staff'
    default = 'default'


class SubRoleEnum(str, Enum):
    creator = 'creator'
    customer = 'customer'
    staff = 'staff'
    instructor = 'instructor'
    client = 'client'
