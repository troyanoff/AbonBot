from time import time
from aiogram.filters import BaseFilter
from aiogram.types import Message
from email_validator import validate_email, EmailNotValidError

from keyboards.inline.factories import CompanyFactory
from core.config import settings


class EmailFilter(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        try:
            validate_email(message.text)
            return True
        except EmailNotValidError:
            return False
