import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    Message, CallbackQuery
)

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import (
    create_simply_inline_kb, create_offset_inline_kb
)
from routers.locations.manage.state_routers.default.handlers import manage
from services.locations import get_location_service
from routers.locations.representation.state import FSMLocationRepr
from schemas.utils import FailSchema
from schemas.representations import (
    CompanyReprSchema,
    LocationListSchema
)
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = FSMLocationRepr.repr
callback_prefix = 'location'


async def locations_repr(
    message: Message,
    lang: str,
    state: FSMContext,
):
    state_handler = f'{router_state.state}:locations_repr'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
    await state.set_state(router_state)

    data = await state.get_data()
    company_uuid = data['company_uuid']

    service = get_location_service()
    locations: LocationListSchema = await service.get_list(
        company_uuid)

    if await st.is_debag():
        logger.info(f'{locations=}')

    core_term_lang: core_Lang = getattr(core_term, lang)
    if isinstance(locations, FailSchema):
        await message.answer(
            text=core_term_lang.terms.error
        )
        await state.clear()
        await state.set_state(default_state)
        return

    terminology_lang: Lang = getattr(terminology, lang)
    if not locations.total_count:
        buttons = terminology_lang.buttons.__dict__
        core_buttons = await core_term_lang.buttons.get_dict_with(
            *FSMLocationRepr.core_buttons)
        buttons.update(core_buttons)

        keyboard = await create_simply_inline_kb(
            buttons,
            1
        )
        await message.answer(
            text=terminology_lang.terms.not_locations,
            reply_markup=keyboard
        )
        return

    if locations.total_count == 1:
        await manage(
            message=message, lang=lang, state=state,
            item=locations.items[0], edit_text=True
        )
        return

    locations_offset = []
    count = 1
    for location in locations.items:
        locations_offset.append(
            {
                'uuid': location.uuid,
                'name': location.name,
                'num': count
            }
        )
        count += 1

    await state.update_data(
        locations_offset=locations_offset
    )

    keyboard = await create_offset_inline_kb(
        data=locations_offset,
        callback_prefix=callback_prefix,
        side_index=0,
        back=False,
        lang=lang,
        additional_buttons=terminology_lang.buttons.__dict__,
    )
    await message.answer(
        text=terminology_lang.terms.locations_list.format(
            company_name=data['company_name']
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
    from routers.locations.create.state_routers.name.handlers \
        import start_create

    await start_create(callback=callback, state=state, lang=lang)


@router.callback_query(
    StateFilter(router_state),
    F.data.regexp((r'^back:\d+$'))
)
async def back(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:back'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    terminology_lang: Lang = getattr(terminology, lang)

    data = await state.get_data()
    locations_offset = data['locations_offset']
    side_index = int(callback.data.split(':')[-1])

    keyboard = await create_offset_inline_kb(
        data=locations_offset,
        callback_prefix=callback_prefix,
        side_index=side_index,
        back=True,
        lang=lang,
        additional_buttons=terminology_lang.buttons.__dict__,
    )

    await callback.message.edit_text(
        text=terminology_lang.terms.locations_list.format(
            company_name=data['company_name']
        ),
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(router_state),
    F.data.regexp((r'^forward:\d+$'))
)
async def forward(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:forward'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    terminology_lang: Lang = getattr(terminology, lang)

    data = await state.get_data()
    locations_offset = data['locations_offset']
    side_index = int(callback.data.split(':')[-1])

    keyboard = await create_offset_inline_kb(
        data=locations_offset,
        callback_prefix=callback_prefix,
        side_index=side_index,
        back=False,
        lang=lang,
        additional_buttons=terminology_lang.buttons.__dict__,
    )

    await callback.message.edit_text(
        text=terminology_lang.terms.locations_list.format(
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
    service = get_location_service()
    location: LocationListSchema = await service.get(
        uuid=uuid)

    if isinstance(location, FailSchema):
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
        state=state, item=location, edit_text=True
    )
