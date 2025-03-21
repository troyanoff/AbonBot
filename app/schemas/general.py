from pydantic import BaseModel
from uuid import UUID

from core.pd_annotations import (
    short_str, empty_short_str, positive_int,
    empty_positive_int, empty_tg_media_id, empty_tg_media_unique_id,
    empty_long_str
)
from schemas.base import MyBaseModel


class ItemNameReprMS(BaseModel):
    name: str
    description: str


class ItemNameCreateMS(BaseModel):
    name: short_str
    description: empty_long_str


class ItemNameUpdateMS(BaseModel):
    name: empty_short_str
    description: empty_long_str


class HumanNameCreateMS(BaseModel):
    tg_id: positive_int
    first_name: short_str
    last_name: short_str


class HumanNameUpdateMS(BaseModel):
    tg_id: empty_positive_int
    first_name: empty_short_str
    last_name: empty_short_str


class HumanNameReprMS(BaseModel):
    tg_id: int
    first_name: str
    last_name: str


class TGPhotoCreateMS(BaseModel):
    photo_id: empty_tg_media_id
    photo_unique_id: empty_tg_media_unique_id


class TGPhotoUpdateMS(BaseModel):
    photo_id: empty_tg_media_id
    photo_unique_id: empty_tg_media_unique_id


class TGPhotoReprMS(BaseModel):
    photo_id: str
    photo_unique_id: str


class ManyUUIDSchema(MyBaseModel):
    uuid_list: list[UUID]
