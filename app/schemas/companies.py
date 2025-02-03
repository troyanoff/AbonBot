from datetime import datetime
from pydantic import Field, EmailStr
from uuid import UUID

from schemas.base import MyBaseModel, MyBaseModelUUID


class CompanyCreateSchema(MyBaseModel):
    """Body to company create."""
    name: str = Field(max_length=50)
    creator_uuid: UUID
    description: str = Field(max_length=300)
    photo_id: str | None = Field(max_length=100, default=None)
    photo_unique_id: str | None = Field(max_length=20, default=None)
    video_id: str | None = Field(max_length=100, default=None)
    video_unique_id: str | None = Field(max_length=20, default=None)
    email: EmailStr


class CompanyUpdateSchema(MyBaseModelUUID):
    """Body to company update."""
    name: str = Field(max_length=50, default='empty')
    creator_uuid: UUID = Field(default='empty')
    description: str = Field(max_length=300, default='empty')
    photo_id: str | None = Field(max_length=100, default='empty')
    photo_unique_id: str | None = Field(max_length=20, default='empty')
    video_id: str | None = Field(max_length=100, default='empty')
    video_unique_id: str | None = Field(max_length=20, default='empty')
    email: EmailStr = Field(default='empty')
