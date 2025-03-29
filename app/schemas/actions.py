from uuid import UUID

from core.pd_annotations import empty_bool, empty_uuid
from schemas.base import MyBaseModel, MinItemSchema
from schemas.general import (
    ItemNameCreateMS, ItemNameUpdateMS, TGPhotoCreateMS, TGPhotoUpdateMS
)


class ActionCreateSchema(MyBaseModel, ItemNameCreateMS, TGPhotoCreateMS):
    """Body to action create."""
    company_uuid: UUID


class ActionUpdateSchema(MinItemSchema, ItemNameUpdateMS, TGPhotoUpdateMS):
    """Body to action update."""
    company_uuid: empty_uuid
    is_archived: empty_bool
