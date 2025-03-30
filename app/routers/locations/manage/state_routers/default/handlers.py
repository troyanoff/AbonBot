import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import (
    create_simply_inline_kb
)
from schemas.representations import (
    LocationReprSchema
)
from services.companies import get_company_service
from routers.locations.manage.state import FSMLocationManage
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_group = FSMLocationManage
router_state = FSMLocationManage.manage


async def manage(
    message: Message,
    lang: str,
    state: FSMContext,
    item: LocationReprSchema,
    edit_text: bool = False
):
    state_handler = f'{router_state.state}:manage'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
    await state.set_state(router_state)

    await state.update_data(
        location_uuid=item.uuid
    )

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    buttons = terminology_lang.buttons.__dict__
    core_buttons = await core_term_lang.buttons.get_dict_with(
        *router_group.core_buttons)
    buttons.update(core_buttons)

    keyboard = await create_simply_inline_kb(
        buttons=buttons,
        width=1
    )
    text = terminology_lang.terms.manage.format(
        name=item.name,
        description=item.description,
        city=item.city,
        street=item.street,
        house=item.house,
        flat=item.flat,
    )
    if edit_text:
        photo = item.photo_id
        if not photo:
            photo = st.stug_photo

        if message.photo:
            media = InputMediaPhoto(
                media=photo,
                caption=text
            )
            await message.edit_media(
                media=media,
                reply_markup=keyboard
            )
            return

        await message.delete()
        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )
        return
    else:
        photo = item.photo_id
        if not photo:
            photo = st.stug_photo
        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )


@router.callback_query(
    StateFilter(router_state),
    F.data == 'update'
)
async def update(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:update'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    from routers.locations.update.state_routers.name.handlers \
        import start
    await start(
        message=callback.message, state=state, lang=lang
    )


@router.callback_query(
    StateFilter(router_state),
    F.data == 'create'
)
async def create(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:create'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    data = await state.get_data()
    if await st.is_debag():
        logger.info(f'\n{'=' * 80}\n{data=}\n{'=' * 80}')

    from routers.locations.create.state_routers.name.handlers \
        import start_create
    await start_create(
        callback=callback, state=state, lang=lang
    )


@router.callback_query(
    StateFilter(router_state),
    F.data == 'back_state'
)
async def back_state(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:back_state'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    from routers.companies.manage.state_routers.default.handlers \
        import manage
    data = await state.get_data()
    service = get_company_service()
    company = await service.get(data['company_uuid'])
    await manage(
        message=callback.message, state=state, lang=lang, company=company,
        edit_text=True
    )
