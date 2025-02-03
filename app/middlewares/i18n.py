import logging

from aiogram import BaseMiddleware
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import TelegramObject, User
from typing import Any, Awaitable, Callable, Dict

from core.config import settings
from keyboards.menu.base import set_client_menu
from services.clients import get_client_service
from states.general import FSMDefault


logger = logging.getLogger(__name__)


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.info('Присваиваем i18n')

        for k, v in data.items():
            logger.info(f'{k} = {v}')
        
        # for k, v in event.__dict__.items():
        #     logger.info(f'{k} = {v}')

        user: User = data.get('event_from_user')
        logger.info(user)

        if user is None:
            return await handler(event, data)

        service = get_client_service()
        client = await service.get(user.id)
        data['client_data'] = client if client else None

        user_lang = user.language_code
        translations = data.get('_translations')
        i18n = translations.get(user_lang, settings.default_lang)
        data['i18n'] = i18n

        if not client:
            bot = data['bots'][0]
            await set_client_menu(bot, user.id, i18n['menu_start'])

        # Нужно перепродумать после тестов.
        current_state = await data['state'].get_state()
        if client and current_state is None:
            logger.info('Ставим дефолтное состояние')
            await data['state'].set_state(FSMDefault.default)
            data['raw_state'] = 'FSMDefault:default'

        return await handler(event, data)