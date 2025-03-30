from uuid import UUID

from core.pd_annotations import empty_uuid, empty_bool
from schemas.base import MyBaseModel, MinItemSchema
from schemas.general import TGPhotoCreateMS, TGPhotoUpdateMS


class InstructorCreateSchema(MyBaseModel, TGPhotoCreateMS):
    """Body to instructor create."""
    company_uuid: UUID
    client_uuid: UUID


class InstructorUpdateSchema(MinItemSchema, TGPhotoUpdateMS):
    """Body to instructor update."""
    company_uuid: empty_uuid
    client_uuid: empty_uuid
    is_archived: empty_bool
