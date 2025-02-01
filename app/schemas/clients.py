
from pydantic import Field, field_validator

from schemas.base import MyBaseModel, SexEnum


class ClientCreateSchema(MyBaseModel):
    """Body to client create."""
    tg_id: int
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    photo_id: str = Field(max_length=100, default=None)
    photo_unique_id: str = Field(max_length=20, default=None)
    sex: SexEnum

