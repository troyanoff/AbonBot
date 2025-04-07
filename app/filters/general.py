from time import time
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
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


class TextFilter(BaseFilter):
    def __init__(self, max_lenght: int) -> None:
        self.max_lenght = max_lenght

    async def __call__(self, message: Message) -> bool:
        result = len(message.text) > self.max_lenght
        if not result:
            return result
        return {'result': message.text}


class TextAlphaFilter(BaseFilter):
    def __init__(self, max_lenght: int) -> None:
        self.max_lenght = max_lenght

    async def __call__(self, message: Message) -> bool:
        result = message.text.isalpha()
        if not result:
            return False
        result = len(message.text) > self.max_lenght
        if result:
            return False
        return {'result': message.text}


class IntegerFilter(BaseFilter):
    def __init__(self, min_: int, max_: int) -> None:
        self.min_ = min_
        self.max_ = max_

    async def __call__(self, message: Message) -> bool:
        try:
            strip_msg = message.text.strip()
            int_text = int(strip_msg)
            result = self.min_ <= int_text <= self.max_
        except Exception:
            return False
        if not result:
            return result
        return {'result': int_text}


class BoolFilter(BaseFilter):
    def __init__(self) -> None:
        self.callbacks = {
            'yes': True,
            'no': False
        }

    async def __call__(self, callback: CallbackQuery) -> bool:
        result = callback.data in self.callbacks
        if not result:
            return False
        return {'result': self.callbacks[callback.data]}


class PhotoFilter(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        if not message.photo:
            return False
        photo = message.photo[-1]
        return {
            'result': {
                'photo_id': photo.file_id,
                'photo_unique_id': photo.file_unique_id
            }
        }


class CallbackFilter(BaseFilter):
    def __init__(self, callbacks: dict) -> None:
        self.callbacks = callbacks

    async def __call__(self, callback: CallbackQuery) -> bool:
        result = callback.data in self.callbacks
        if not result:
            return False
        return {'result': self.callbacks[callback.data]}
