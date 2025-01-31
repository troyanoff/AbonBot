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
from db import redis


logger = logging.getLogger(__name__)


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    redis_init = Redis(host=settings.redis_host, port=settings.redis_port)

    redis.redis = redis_init
    storage = RedisStorage(redis=redis_init)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    dp = Dispatcher(storage=storage)

    # dp.workflow_data.update(...)

    # Настраиваем главное меню бота
    # await set_main_menu(bot)

    # Регистриуем роутеры
    logger.info('Подключаем роутеры')
    # ...

    # Регистрируем миддлвари
    logger.info('Подключаем миддлвари')
    # ...

    # Пропускаем накопившиеся апдейты и запускаем polling
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())