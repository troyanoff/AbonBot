import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from importlib import import_module

from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from handlers.base import RequestTG
from schemas.representations import ClientReprSchema
from routers.default.state import FSMDefault
from routers.companies.representation.state import FSMCompanyRepr
from routers.companies.representation.state_routers.repr.handlers import \
    handler
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()


@router.message(Command(commands='companies'))
async def companies_command(
    message: Message,
    lang: str,
    client_data: ClientReprSchema,
    state: FSMContext,
):
    state_handler = 'general:companies'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    await state.set_data(
        {
            'client_uuid': client_data.uuid,
            'state_path': []
        }
    )
    request_tg = RequestTG(update=message, lang=lang, state=state)
    await handler(request_tg)


@router.message(Command(commands='learn'))
async def learn(
    message: Message,
    lang: str,
    state: FSMContext,
):
    state_handler = 'general:learn'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    terminology_lang: Lang = getattr(terminology, lang)
    await message.answer(
        text=terminology_lang.terms.learn
    )


@router.message(Command(commands='support'))
async def support(
    message: Message,
    lang: str
):
    state_handler = 'general:support'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
    terminology_lang: Lang = getattr(terminology, lang)

    await message.answer(
        text=terminology_lang.terms.support
    )


@router.message(Command(commands='profile'))
async def profile(
    message: Message,
    lang: str,
    state: FSMContext,
    client_data: ClientReprSchema
):
    state_handler = 'general:profile'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
    await state.update_data(client_uuid=client_data.uuid)

    path = 'routers.clients.profile.state_routers.default.handlers.handler'
    module_path, caller = path.rsplit('.', 1)
    module = import_module(module_path)
    request_tg = RequestTG(update=message, lang=lang, state=state)
    await getattr(module, caller)(request_tg)
