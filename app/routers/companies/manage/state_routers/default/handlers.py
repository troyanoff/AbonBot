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
from schemas.representations import ClientReprSchema, CompanyReprSchema
from services.companies import get_company_service
from routers.companies.manage.state import FSMCompanyManage
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMCompanyManage.manage


async def manage(
    message: Message,
    lang: str,
    state: FSMContext,
    company: CompanyReprSchema = None,
    uuid: str = None,
    edit_text: bool = False
):
    state_handler = f'{router_state.state}:manage'
    logger.info(state_handler)
    await state.set_state(router_state)

    if not company and not uuid:
        raise Exception()

    if not company:
        service = get_company_service()
        company = await service.get(uuid)

    await state.update_data(
        company_uuid=company.uuid,
        company_name=company.name
    )

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    buttons = terminology_lang.buttons.__dict__
    core_buttons = await core_term_lang.buttons.get_dict_with(
        *FSMCompanyManage.core_buttons)
    buttons.update(core_buttons)

    keyboard = await create_simply_inline_kb(
        buttons=buttons,
        width=1
    )
    text = terminology_lang.terms.manage.format(
        name=company.name,
        description=company.description,
        email=company.email,
        max_hour_cancel=company.max_hour_cancel,
    )
    if edit_text:
        photo = company.photo_id
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
        photo = company.photo_id
        if not photo:
            photo = st.stug_photo
        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )


@router.callback_query(
    StateFilter(router_state),
    F.data == 'update_company'
)
async def update_profile(
    callback: CallbackQuery,
    state: FSMContext,
    client_data: ClientReprSchema,
    lang: str
):
    state_handler = f'{router_state.state}:update_company'
    logger.info(state_handler)

    from routers.companies.update.state_routers.name.handlers \
        import start_update
    await start_update(
        message=callback.message, state=state, lang=lang,
        client_data=client_data
    )
