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
from schemas.base import SubRoleEnum
from schemas.representations import (
    SubscriptionReprSchema
)
from routers.subscriptions.manage_company.state import states_group
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_group = states_group
router_state = states_group.manage


async def manage(
    message: Message,
    lang: str,
    state: FSMContext,
    item: SubscriptionReprSchema,
    edit_text: bool = False
):
    state_handler = f'{router_state.state}:manage'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
    await state.set_state(router_state)

    await state.update_data(
        subscription_uuid=item.uuid
    )

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    buttons = terminology_lang.buttons.__dict__

    if item.role == SubRoleEnum.instructor:
        buttons.pop('add_instructor', None)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *router_group.core_buttons)
    buttons.update(core_buttons)

    keyboard = await create_simply_inline_kb(
        buttons=buttons,
        width=1
    )
    sex = getattr(core_term_lang.terms, item.client.sex.name)
    text = terminology_lang.terms.manage.format(
        first_name=item.client.first_name,
        last_name=item.client.last_name,
        sex=sex,
    )
    if edit_text:
        photo = item.client.photo_id
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
        photo = item.client.photo_id
        if not photo:
            photo = st.stug_photo
        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )


@router.callback_query(
    StateFilter(router_state),
    F.data == 'issuance'
)
async def issuance(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:issuance'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    # from routers.locations.update.state_routers.name.handlers \
    #     import start
    # await start(
    #     message=callback.message, state=state, lang=lang
    # )


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

    from routers.subscriptions.create.state_routers.client.handlers \
        import start
    await start(
        callback=callback, state=state, lang=lang
    )


@router.callback_query(
    StateFilter(router_state),
    F.data == 'add_instructor'
)
async def add_instructor(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:add_instructor'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'\n{'=' * 80}\n{data=}\n{'=' * 80}')

    from routers.instructors.create.state_routers.photo.handlers \
        import start
    await start(
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
    await manage(
        message=callback.message, state=state, lang=lang,
        uuid=data['company_uuid'],
        edit_text=True
    )
