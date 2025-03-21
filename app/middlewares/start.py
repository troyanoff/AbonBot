import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from typing import Any, Awaitable, Callable, Dict

from keyboards.menu.base import set_client_menu
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
        # for k, v in data.items():
        #     logger.info(f'{k} = {v}')

        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        client = data['client_data']

        i18n = data['i18n']
        bot = data['bots'][0]
        data['bot'] = bot

        if not client:
            await set_client_menu(bot, user.id, i18n['menu_start'])

        return await handler(event, data)
