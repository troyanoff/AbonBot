
from aiogram import Router
from aiogram.types import Message

from phrases.ru import phrases


router = Router()

@router.message()
async def send_echo(message: Message, i18n: dict):
    await message.reply(text=i18n['phrases']['deadlock'])