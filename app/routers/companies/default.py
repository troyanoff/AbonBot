import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards.inline.base import create_inline_kb
from keyboards.inline.factories import company_inline, CompanyFactory
from services.companies import get_company_service
from states.general import FSMClientUpdate, FSMStart, FSMDefault
from schemas.representations import ClientReprSchema


logger = logging.getLogger(__name__)

router = Router()


@router.message(Command(commands='companies'), StateFilter(FSMDefault.default))
async def companies_command(
    message: Message,
    i18n: dict,
    client_data: ClientReprSchema
):
    buttons_list = ('manage_company', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list,
        cancel_button=False
    )
    if not client_data.companies_count:
        await message.answer(
            text=i18n['phrases']['company_empty'],
            reply_markup=keyboard
        )
        return
    service = get_company_service()
    companies = await service.get_list(client_data.uuid)
    keyboard = await company_inline(
        client_data.tg_id, companies, i18n['buttons']['cancel']
    )

    text = i18n['phrases']['company_header']

    await message.answer(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(
    CompanyFactory.filter(),
    StateFilter(FSMDefault.default)
)
async def company(
    callback: CallbackQuery,
    callback_data: CompanyFactory,
    i18n: dict,
    client_data: ClientReprSchema
):
    logger.info('company handler')
    await callback.message.answer(text=callback_data.pack())
