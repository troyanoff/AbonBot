from schemas.api import ResponseShema
from schemas.base import MyBaseModel


class ExceptSchema(MyBaseModel):
    msg: str
    exc: str = 'None'


class FailSchema(MyBaseModel):
    response: ResponseShema = None


class DoneSchema(MyBaseModel):
    response: ResponseShema = None
