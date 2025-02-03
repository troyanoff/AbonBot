import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from time import time
from typing import Any, Awaitable, Callable, Dict

from core.config import settings


logger = logging.getLogger(__name__)


class CallbackAnswerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.info('Отвечаем на колбэк')
        await event.answer()

        if settings.callback_sep in event.data:
            callback_time = int(event.data.split(':')[1])
            now = int(time())
            if now - callback_time > settings.callback_ttl:
                logger.info(f'Сейчас {now}, колбек создан в {callback_time}')
                return

        return await handler(event, data)