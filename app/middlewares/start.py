import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from typing import Any, Awaitable, Callable, Dict

from keyboards.menu.base import set_main_menu
from services.clients import get_client_service


logger = logging.getLogger(__name__)


class ClientCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.info('Проверяем регистрацию у клиента.')

        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        service = get_client_service()
        client = await service.get(user.id)
        logger.info(client)
        data['client_data'] = client if client else None

        i18n = data['i18n']
        bot = data['bots'][0]
        data['bot'] = bot

        if client:
            await set_main_menu(bot, i18n['menu'])
        else:
            await set_main_menu(bot, i18n['menu_start'])

        return await handler(event, data)