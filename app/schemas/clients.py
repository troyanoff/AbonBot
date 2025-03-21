
from pydantic import field_validator

from core.pd_annotations import false_bool, empty_sex, empty_bool
from schemas.base import MyBaseModel, SexEnum, MinItemSchema
from schemas.general import (
    HumanNameCreateMS, HumanNameUpdateMS, TGPhotoCreateMS, TGPhotoUpdateMS
)


class ClientCreateSchema(MyBaseModel, HumanNameCreateMS, TGPhotoCreateMS):
    """Body to client create."""
    sex: SexEnum
    is_premium: false_bool

    @field_validator('is_premium', mode='after')
    @classmethod
    def check_is_premium(cls, value: bool) -> bool:
        if value:
            raise ValueError('is_premium must be False')
        return value


class ClientUpdateSchema(MinItemSchema, HumanNameUpdateMS, TGPhotoUpdateMS):
    """Body to client update."""
    sex: empty_sex
    is_premium: empty_bool
