from schemas.base import MyBaseModel


class Login(MyBaseModel):
    login: str
    password: str


class ResponseShema(MyBaseModel):
    status: int
    data: list | dict | str
    ttc: float = 0.0
