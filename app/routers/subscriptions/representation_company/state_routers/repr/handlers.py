import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery, InputMediaPhoto, Message
)

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import (
    create_simply_inline_kb, pages_inline_kb
)
from routers.subscriptions.manage_company.state_routers.default.handlers \
    import manage
from services.subscriptions import get_subscription_service
from services.companies import get_company_service
from routers.actions.representation.state import states_group
from schemas.utils import FailSchema
from schemas.representations import (
    SubscriptionReprSchema,
    SubscriptionListSchema
)
from .terminology import terminology, Lang
from .utils import create_page


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.repr
callback_prefix = 'subscription'


async def start(
    message: Message,
    lang: str,
    state: FSMContext,
):
    state_handler = f'{router_state.state}:start'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
    await state.set_state(router_state)

    data = await state.get_data()
    company_uuid = data['company_uuid']

    service = get_subscription_service()
    items: SubscriptionListSchema = await service.get_list(
        company_uuid)

    core_term_lang: core_Lang = getattr(core_term, lang)
    if isinstance(items, FailSchema):
        await message.answer(
            text=core_term_lang.terms.error
        )
        await state.clear()
        await state.set_state(default_state)
        return

    terminology_lang: Lang = getattr(terminology, lang)
    if not items.total_count:
        buttons = terminology_lang.buttons.__dict__
        core_buttons = await core_term_lang.buttons.get_dict_with(
            *states_group.core_buttons)
        buttons.update(core_buttons)

        keyboard = await create_simply_inline_kb(
            buttons,
            1
        )
        if not message.photo:
            await message.answer_photo(
                photo=st.stug_photo,
                caption=terminology_lang.terms.not_items,
                reply_markup=keyboard
            )
            return
        await message.edit_media(
            media=InputMediaPhoto(
                media=st.stug_photo,
                caption=terminology_lang.terms.not_items
            ),
            reply_markup=keyboard
        )
        return

    data_pages, page = await create_page(
        company_uuid=company_uuid,
        lang=lang,
        message=message,
        state=state,
    )
    keyboard = await pages_inline_kb(
        data=data_pages,
        callback_prefix=callback_prefix,
        page=page,
        total_count=items.total_count,
        lang=lang,
        additional_buttons=terminology_lang.buttons.__dict__
    )

    if not message.photo:
        await message.answer_photo(
            photo=st.stug_photo,
            caption=terminology_lang.terms.list_items.format(
                company_name=data['company_name']
            ),
            reply_markup=keyboard
        )
        return
    await message.edit_media(
        media=InputMediaPhoto(
            media=st.stug_photo,
            caption=terminology_lang.terms.list_items.format(
                company_name=data['company_name']
            )
        ),
        reply_markup=keyboard
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

    from routers.subscriptions.create.state_routers.client.handlers\
        import start

    await start(callback=callback, state=state, lang=lang)


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


@router.callback_query(
    StateFilter(router_state),
    F.data.regexp((r'^back:\d+:\d+$'))
)
async def back(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:back'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    terminology_lang: Lang = getattr(terminology, lang)

    split_data = callback.data.split(':')
    total_count = int(split_data[1])
    page = int(split_data[2]) - 1  # back handler

    data = await state.get_data()
    company_uuid = data['company_uuid']

    pages_data, page = await create_page(
        company_uuid=company_uuid,
        total_count=total_count,
        page=page,
        lang=lang,
        message=callback.message,
        state=state,
    )

    keyboard = await pages_inline_kb(
        data=pages_data,
        callback_prefix=callback_prefix,
        page=page,
        total_count=total_count,
        lang=lang,
        additional_buttons=terminology_lang.buttons.__dict__,
    )

    await callback.message.edit_caption(
        caption=terminology_lang.terms.list_items.format(
            company_name=data['company_name']
        ),
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(router_state),
    F.data.regexp((r'^forward:\d+:\d+$'))
)
async def forward(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:forward'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    terminology_lang: Lang = getattr(terminology, lang)

    split_data = callback.data.split(':')
    total_count = int(split_data[1])
    page = int(split_data[2]) + 1  # forward handler

    data = await state.get_data()
    company_uuid = data['company_uuid']

    pages_data, page = await create_page(
        company_uuid=company_uuid,
        total_count=total_count,
        page=page,
        lang=lang,
        message=callback.message,
        state=state,
    )
    logger.info(pages_data)

    keyboard = await pages_inline_kb(
        data=pages_data,
        callback_prefix=callback_prefix,
        page=page,
        total_count=total_count,
        lang=lang,
        additional_buttons=terminology_lang.buttons.__dict__,
    )

    await callback.message.edit_caption(
        caption=terminology_lang.terms.list_items.format(
            company_name=data['company_name']
        ),
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(router_state),
    F.data.regexp((
        r'^'
        + f'{callback_prefix}'
        + r':[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-'
        + r'[0-9a-f]{12}$'
    ))
)
async def to_manage(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:to_manage'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    uuid = callback.data.split(':')[-1]
    service = get_subscription_service()
    item: SubscriptionReprSchema = await service.get(
        uuid=uuid)

    if isinstance(item, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await callback.message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(default_state)
        return

    await manage(
        message=callback.message, lang=lang,
        state=state, item=item, edit_text=True
    )
