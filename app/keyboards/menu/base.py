from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot, menu: dict):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in menu.items()
    ]
    await bot.set_my_commands(main_menu_commands)
