import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from typing import Any, Awaitable, Callable, Dict

from core.config import settings as st
from core.terminology import Lang, terminology
from keyboards.menu.base import set_client_menu
from services.clients import get_client_service
from states.general import FSMDefault


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

        # if settings.callback_sep in event.data:
        #     callback_time = int(event.data.split(':')[1])
        #     now = int(time())
        #     if now - callback_time > settings.callback_ttl:
        #         logger.info(f'Сейчас {now}, колбек создан в {callback_time}')
        #         return

        logger.info(f'\n{'=' * 80}\ncallback={event.data}\n{'=' * 80}')
        return await handler(event, data)


class ClientMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.info('Cet client data')

        # for k, v in data.items():
        #     logger.info(f'{k} = {v}')

        # for k, v in event.__dict__.items():
        #     logger.info(f'{k} = {v}')

        user: User = data.get('event_from_user')
        logger.info(f'{user=}')

        if user is None:
            return await handler(event, data)

        service = get_client_service()
        client = await service.get(user.id)

        logger.info(f'actual_{client=}')
        data['client_data'] = client if client else None
        return await handler(event, data)


class LangMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.info('Get user lang')

        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        user_lang = user.language_code
        lang = (
            user_lang if user_lang in st.supported_langs else st.default_lang
        )
        data['lang'] = lang
        return await handler(event, data)


class NotClientMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.info('Check state')

        client = data['client_data']
        lang = data['lang']

        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        if not client:
            terminology_lang: Lang = getattr(terminology, lang)
            bot = data['bots'][0]
            await set_client_menu(
                bot, user.id, terminology_lang.menu_start.__dict__)

        # Нужно перепродумать после тестов.
        current_state = await data['state'].get_state()
        if client and current_state is None:
            logger.info('Set default state')
            await data['state'].set_state(FSMDefault.default)
            data['raw_state'] = 'FSMDefault:default'

        logger.info(f'\n{'=' * 80}\nstate={data['raw_state']}\n{'=' * 80}')
        return await handler(event, data)
