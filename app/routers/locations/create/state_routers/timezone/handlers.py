import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from services.locations import get_location_service
from schemas.locations import LocationCreateSchema
from schemas.utils import FailSchema, DoneSchema
from routers.locations.create.state import FSMLocationCreate
# from routers.locations.manage.state_routers.default.handlers import manage
from routers.default.state import FSMDefault
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_group = FSMLocationCreate
router_state = router_group.timezone
# next_state = FSMLocationManage.manage


@router.message(
    StateFilter(router_state),
    F.text.regexp(r'^-?\d+$'),
    lambda msg: -12 <= int(msg.text) <= 14
)
async def done(
    message: Message, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:done'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    data = await state.get_data()
    new_location_dict = data['new_location']
    new_location_dict['timezone'] = int(message.text)
    await state.update_data(
        new_location=new_location_dict
    )

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    service = get_location_service()
    result: DoneSchema = await service.create(
        LocationCreateSchema.model_validate(new_location_dict))

    if isinstance(result, FailSchema):
        await message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    await message.answer(
        text=terminology_lang.terms.done,
        reply_markup=None
    )
    del data['new_location']
    await state.update_data(**data)
    location = await service.get(result.response.data['item']['uuid'])
    # await manage(
    #     message=message, lang=lang, state=state, location=location
    # )


@router.message(
    StateFilter(router_state)
)
async def error(
    message: Message, lang: str
):
    state_handler = f'{router_state.state}:error'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *router_group.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.error,
        reply_markup=keyboard
    )
