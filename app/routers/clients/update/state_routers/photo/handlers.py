import logging

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PhotoSize

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from services.clients import get_client_service
from schemas.representations import ClientReprSchema
from routers.clients.update.state import FSMClientUpdate
from routers.default.state import FSMDefault
from .terminology import terminology, Lang
from ..gender.terminology import terminology as last_term, Lang as last_Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMClientUpdate.photo


@router.message(
    StateFilter(router_state),
    F.photo[-1].as_('largest_photo')
)
async def done(
    message: Message, state: FSMContext, lang: str,
    largest_photo: PhotoSize, bot: Bot,
    client_data: ClientReprSchema
):
    state_handler = f'{router_state.state}:done'
    logger.info(state_handler)

    await state.update_data(
        uuid=client_data.uuid.__str__(),
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )

    data = await state.get_data()

    if await st.is_debag():
        logger.info(f'{state_handler} {data=}')

    service = get_client_service()
    result = await service.update(message.from_user.id, data)

    if not result:
        core_term_lang: core_Lang = getattr(core_term, lang)
        await message.answer(
            text=core_term_lang.terms.error
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    terminology_lang: Lang = getattr(terminology, lang)
    await message.answer(
        text=terminology_lang.terms.done
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.callback_query(
    StateFilter(router_state),
    F.data == FSMClientUpdate.miss_button
)
async def miss_state(
    callback: CallbackQuery, state: FSMContext, lang: str,
    client_data: ClientReprSchema
):
    state_handler = f'{router_state.state}:miss_state'
    logger.info(state_handler)

    await state.update_data(
        uuid=client_data.uuid.__str__()
    )

    data = await state.get_data()
    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    service = get_client_service()
    result = await service.update(callback.from_user.id, data)
    if not result:
        core_term_lang: core_Lang = getattr(core_term, lang)
        await callback.message.edit_text(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    terminology_lang: Lang = getattr(terminology, lang)
    await callback.message.edit_text(
        text=terminology_lang.terms.done
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.callback_query(
    StateFilter(router_state),
    F.data.in_(FSMClientUpdate.photo_callbacks)
)
async def cancel_photo(
    callback: CallbackQuery, state: FSMContext, lang: str,
    client_data: ClientReprSchema
):
    state_handler = f'{router_state.state}:cancel_photo'
    logger.info(state_handler)

    await state.update_data(
        uuid=client_data.uuid.__str__(),
        photo_unique_id='',
        photo_id=''
    )

    data = await state.get_data()

    if await st.is_debag():
        logger.info(f'{state_handler} {data=}')

    service = get_client_service()
    result = await service.update(callback.from_user.id, data)
    if not result:
        core_term_lang: core_Lang = getattr(core_term, lang)
        await callback.message.edit_text(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    terminology_lang: Lang = getattr(terminology, lang)
    await callback.message.edit_text(
        text=terminology_lang.terms.done
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.message(
    StateFilter(router_state)
)
async def error(
    message: Message, lang: str
):
    state_handler = f'{router_state.state}:error'
    logger.info(state_handler)

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)
    last_term_lang: last_Lang = getattr(last_term, lang)

    buttons = last_term_lang.buttons.__dict__
    core_buttons = await core_term_lang.buttons.get_dict_with(
        *FSMClientUpdate.core_buttons)
    buttons.update(core_buttons)

    keyboard = await create_simply_inline_kb(
        buttons,
        1
    )

    await message.answer(
        text=terminology_lang.terms.error,
        reply_markup=keyboard
    )
