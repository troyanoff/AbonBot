import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from typing import Any, Awaitable, Callable, Dict

from core.config import settings
from keyboards.menu.base import set_main_menu
from services.clients import get_client_service


logger = logging.getLogger(__name__)


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.info('Присваиваем i18n')
        # for k, v in data.items():
        #     logger.info(f'{k} = {v}')

        user: User = data.get('event_from_user')
        logger.info(user)

        if user is None:
            return await handler(event, data)

        user_lang = user.language_code
        translations = data.get('_translations')
        i18n = translations.get(user_lang, settings.default_lang)
        data['i18n'] = i18n

        return await handler(event, data)