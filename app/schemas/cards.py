from pydantic import model_validator
from typing_extensions import Self
from uuid import UUID

from core.pd_annotations import (
    empty_positive_int, false_bool, empty_uuid, empty_bool,
    empty_time, none_empty_time
)
from schemas.base import MyBaseModel, MinItemSchema
from schemas.general import ItemNameCreateMS, ItemNameUpdateMS


class CardCreateSchema(MyBaseModel, ItemNameCreateMS):
    """Body to card create."""
    company_uuid: UUID
    by_delta: false_bool
    month_delta: empty_positive_int
    by_count: false_bool
    count: empty_positive_int
    by_limit: false_bool
    time_limit: empty_time
    freeze: false_bool
    freezing_days: empty_positive_int

    @model_validator(mode='after')
    def check_card_value(self) -> Self:
        if not (self.by_count or self.by_delta):
            raise ValueError('card type is not specified')
        # if not self.by_delta and self.by_limit:
        #     raise ValueError(
        #         'Card type without by_delta should not have by_limit')
        if self.by_delta and not self.month_delta:
            raise ValueError('card with by_delta must have month_delta')
        if self.by_count and not self.count:
            raise ValueError('card with by_count must have count')
        if self.freeze and not self.by_delta:
            raise ValueError('card with freeze must have by_delta')
        if self.freeze and not self.freezing_days:
            raise ValueError('card with freeze must have freezing_days')
        if self.by_limit and not self.time_limit:
            raise ValueError('card with by_limit must have time_limit')
        return self


class CardEventCreateShema(MyBaseModel):
    company_uuid: UUID
    card_uuid: UUID
    event_uuid_list: list[UUID]


class CardUpdateSchema(MinItemSchema, ItemNameUpdateMS):
    """Body to card update."""
    company_uuid: empty_uuid
    by_delta: empty_bool
    month_delta: empty_positive_int
    by_count: empty_bool
    count: empty_positive_int
    by_limit: empty_bool
    time_limit: none_empty_time
    freeze: empty_bool
    freezing_days: empty_positive_int
    is_archived: empty_bool
