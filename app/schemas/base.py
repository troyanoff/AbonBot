import orjson

from datetime import datetime
from enum import Enum
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class MyBaseModel(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        populate_by_name = True


class MyBaseModelRepr(BaseModel):
    uuid: str
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
    uuid: str

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


class CreateFieldEnum(str, Enum):
    start = 'start'
    default = 'default'
    end = 'end'
