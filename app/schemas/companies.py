from pydantic import EmailStr, field_validator
from uuid import UUID

from core.pd_annotations import empty_non_negative_int, empty_email
from schemas.base import MyBaseModel, MinItemSchema
from schemas.general import (
    ItemNameCreateMS, ItemNameUpdateMS, TGPhotoCreateMS, TGPhotoUpdateMS
)


class CompanyCreateSchema(MyBaseModel, ItemNameCreateMS, TGPhotoCreateMS):
    """Body to company create."""
    creator_uuid: UUID
    email: EmailStr
    max_hour_cancel: empty_non_negative_int

    @field_validator('max_hour_cancel', mode='after')
    @classmethod
    def check_max_hour_cancel(cls, value: int) -> int:
        if value > 24:
            raise ValueError('Too many hours for max_hour_cancel')
        return value


class CompanyUpdateSchema(MinItemSchema, ItemNameUpdateMS, TGPhotoUpdateMS):
    """Body to company update."""
    email: empty_email
    max_hour_cancel: empty_non_negative_int

    @field_validator('max_hour_cancel', mode='after')
    @classmethod
    def check_max_hour_cancel(cls, value: int) -> int:
        if value > 24:
            raise ValueError('Too many hours for max_hour_cancel')
        return value
