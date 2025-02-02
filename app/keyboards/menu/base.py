from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_client_menu(bot: Bot, client_id: int, menu: dict):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in menu.items()
    ]
    await bot.set_my_commands(
        main_menu_commands,
        scope=BotCommandScopeChat(chat_id=client_id))
