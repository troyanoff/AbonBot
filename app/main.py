import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton,
    InlineKeyboardMarkup, Message, PhotoSize
)
from redis.asyncio import Redis

from core.config import settings

from routers import router
from routers.auxiliaries import deadlock, start_bot
from routers.default import default
from routers.companies import default as default_company, create_company

from db import redis

from middlewares.general import CallbackAnswerMiddleware
from middlewares.i18n import TranslatorMiddleware
from middlewares.start import ClientCheckMiddleware

from phrases.general import translations


logger = logging.getLogger(__name__)


async def on_startup(dp):
    print("Бот запущен!")


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    logger.info(f'CONFIG {settings}')

    redis_init = Redis(host=settings.redis_host, port=settings.redis_port)

    async for key in redis_init.scan_iter("fsm:*"):
        print(key)
        await redis_init.delete(key)

    redis.redis = redis_init
    storage = RedisStorage(redis=redis_init)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=storage)

    # dp.workflow_data.update(...)

    # Регистриуем роутеры
    logger.info('Подключаем роутеры')
    dp.include_router(start_bot.router)

    dp.include_router(router)

    dp.include_router(default.router)

    dp.include_router(default_company.router)
    dp.include_router(create_company.router)

    dp.include_router(deadlock.router)

    # Регистрируем миддлвари
    logger.info('Подключаем миддлвари')
    dp.update.middleware(TranslatorMiddleware())
    dp.callback_query.outer_middleware(CallbackAnswerMiddleware())
    start_bot.router.message.middleware(ClientCheckMiddleware())

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(
            bot, _translations=translations)
    finally:
        logger.info('Прерываем соединение с redis')
        await redis_init.aclose()


asyncio.run(main())
