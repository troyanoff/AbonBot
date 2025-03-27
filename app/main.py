import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from core.config import settings
from db import redis
from middlewares.general import (
    CallbackAnswerMiddleware, ClientMiddleware, LangMiddleware,
    NotClientMiddleware
)
from routers import router


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

    logger.info('Including routers')
    dp.include_router(router)

    logger.info('Including middlewares')
    dp.update.middleware(ClientMiddleware())
    dp.update.middleware(LangMiddleware())
    dp.update.middleware(NotClientMiddleware())
    dp.callback_query.outer_middleware(CallbackAnswerMiddleware())

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(
            bot)
    finally:
        logger.info('Прерываем соединение с redis')
        await redis_init.aclose()


asyncio.run(main())
