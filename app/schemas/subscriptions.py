from pydantic import field_validator
from uuid import UUID

from core.pd_annotations import client_sub_role, empty_sub_role, empty_uuid
from schemas.base import SubRoleEnum
from schemas.base import MyBaseModel, MinItemSchema


class SubscriptionCreateSchema(MyBaseModel):
    """Body to subscription create."""
    client_uuid: UUID
    company_uuid: UUID
    role: client_sub_role

    @field_validator('role', mode='after')
    @classmethod
    def check_start_at(cls, value: SubRoleEnum) -> SubRoleEnum:
        if value not in (SubRoleEnum.client, SubRoleEnum.staff):
            raise ValueError('you can only specify client or staff')
        return value


class SubscriptionUpdateSchema(MinItemSchema):
    """Body to subscription update."""
    client_uuid: empty_uuid
    company_uuid: empty_uuid
    role: empty_sub_role

    @field_validator('role', mode='after')
    @classmethod
    def check_start_at(cls, value: SubRoleEnum) -> SubRoleEnum:
        if value and value not in (SubRoleEnum.client, SubRoleEnum.staff):
            raise ValueError('you can only specify client or staff')
        return value
