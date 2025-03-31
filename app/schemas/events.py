from uuid import UUID

from core.pd_annotations import empty_uuid, empty_bool
from schemas.base import MyBaseModel, MinItemSchema


class EventCreateSchema(MyBaseModel):
    """Body to event create."""
    company_uuid: UUID
    location_uuid: UUID
    action_uuid: UUID
    is_personal: bool


class EventUpdateSchema(MinItemSchema):
    """Body to event update."""
    company_uuid: empty_uuid
    location_uuid: empty_uuid
    action_uuid: empty_uuid
    is_personal: empty_bool
