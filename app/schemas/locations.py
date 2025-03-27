from pydantic import field_validator
from uuid import UUID

from core.pd_annotations import (
    short_str, empty_short_str, empty_int
)
from schemas.base import MyBaseModel, MinItemSchema
from schemas.general import (
    ItemNameCreateMS, ItemNameUpdateMS, TGPhotoCreateMS, TGPhotoUpdateMS
)


class LocationCreateSchema(MyBaseModel, ItemNameCreateMS, TGPhotoCreateMS):
    """Body to location create."""
    company_uuid: UUID
    city: short_str
    street: short_str
    house: short_str
    flat: short_str
    timezone: int

    @field_validator('timezone', mode='after')
    @classmethod
    def check_timezone(cls, value: int) -> int:
        if not -12 <= value <= 14:
            raise ValueError('Timezone must be between -12 and 14')
        return value


class LocationUpdateSchema(MinItemSchema, ItemNameUpdateMS, TGPhotoUpdateMS):
    """Body to location update."""
    city: empty_short_str
    street: empty_short_str
    house: empty_short_str
    flat: empty_short_str
    timezone: empty_int

    @field_validator('timezone', mode='after')
    @classmethod
    def check_timezone(cls, value: int) -> int:
        if value and not -12 <= value <= 14:
            raise ValueError('Timezone must be between -12 and 14')
        return value
