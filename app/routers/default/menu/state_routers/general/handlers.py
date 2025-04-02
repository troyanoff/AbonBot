import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
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

    # await state.clear()
    await state.set_state(FSMCompanyRepr.repr)
    await handler(
        update=message, state=state, lang=lang)


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

    await state.set_state(FSMDefault.default)

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)
    keyboard = await create_simply_inline_kb(
        buttons=terminology_lang.buttons.__dict__,
        width=1
    )
    sex = getattr(core_term_lang.terms, client_data.sex.name)
    text = terminology_lang.terms.profile.format(
        first_name=client_data.first_name,
        last_name=client_data.last_name,
        sex=sex,
        companies_count=0,  # to do
        subs_count=0  # to do
    )
    if not client_data.photo_id:
        await message.answer(
            text=text,
            reply_markup=keyboard
        )
        return
    await message.answer_photo(
        photo=client_data.photo_id,
        caption=text,
        reply_markup=keyboard
    )
