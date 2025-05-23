from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from time import time

from core.config import settings
from schemas.representations import CompanyReprSchema


class BaseFactory(CallbackData, prefix='', sep=settings.callback_sep):
    create_at: int

class CompanyFactory(BaseFactory, prefix='com'):
    uuid: str
    creator_tg_id: int


async def company_inline(
    creator: int, companies: list[CompanyReprSchema], cancel_text: str
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for company in companies:
        button = InlineKeyboardButton(
            text=company.name,
            callback_data=CompanyFactory(
                uuid=company.uuid,
                creator_tg_id=creator,
                create_at=int(time())
            ).pack()
        )
        buttons.append(button)
    kb_builder.row(*buttons, width=1)
    kb_builder.row(InlineKeyboardButton(
        text=cancel_text,
        callback_data='cancel'
    ))

    return kb_builder.as_markup()
