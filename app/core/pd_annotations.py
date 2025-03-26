from datetime import datetime, time
from pydantic import Field, EmailStr
from typing import Annotated
from uuid import UUID

from core.config import settings
from schemas.base import SexEnum, SubRoleEnum


# String
short_str = Annotated[
    str,
    Field(max_length=settings.short_field_len)
]
empty_short_str = Annotated[
    str,
    Field(max_length=settings.short_field_len, default='')
]

long_str = Annotated[
    str,
    Field(max_length=settings.long_field_len)
]
empty_long_str = Annotated[
    str,
    Field(max_length=settings.long_field_len, default='')
]
empty_tg_media_id = Annotated[
    str,
    Field(
        max_length=settings.tg_media_id_len,
        default=''
    )
]
empty_tg_media_unique_id = Annotated[
    str,
    Field(
        max_length=settings.tg_media_unique_id_len,
        default=''
    )
]


# Integer
empty_int = Annotated[
    int,
    Field(default=0)
]
positive_int = Annotated[
    int,
    Field(gt=0)
]
empty_positive_int = Annotated[
    int,
    Field(gt=0, default=0)
]
empty_non_negative_int = Annotated[
    int,
    Field(ge=0, default=0)
]

# Boolean
false_bool = Annotated[
    bool,
    Field(default=False)
]
true_bool = Annotated[
    bool,
    Field(default=True)
]
empty_bool = Annotated[
    bool,
    Field(default=None)
]


# Datetime
empty_time = Annotated[
    time,
    Field(default=None)
]
none_empty_time = Annotated[
    time | None,
    Field(default=None)
]
empty_datatime = Annotated[
    datetime,
    Field(default=None)
]
none_empty_datetime = Annotated[
    datetime | None,
    Field(default=None)
]


# UUID
empty_uuid = Annotated[
    UUID,
    Field(default=None)
]
empty_list_uuid = Annotated[
    list[UUID],
    Field(default=None)
]

# Email
empty_email = Annotated[
    EmailStr,
    Field(default=None)
]

# My types
empty_sex = Annotated[
    SexEnum,
    Field(default=None)
]
client_sub_role = Annotated[
    SubRoleEnum,
    Field(default=SubRoleEnum.client)
]
empty_sub_role = Annotated[
    SubRoleEnum,
    Field(default=None)
]
