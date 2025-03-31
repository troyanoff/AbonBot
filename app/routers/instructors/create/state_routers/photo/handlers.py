import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PhotoSize

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from routers.instructors.create.state import states_group
from .terminology import terminology, Lang
from ..end.handlers import end_create


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.photo


async def start(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:start'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    data = await state.get_data()

    await callback.answer()
    await state.update_data(
        new_instructor={
            'company_uuid': data['company_uuid'],
            'client_uuid': data['sub_client_uuid']
        }
    )

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *states_group.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await callback.message.answer(
        text=terminology_lang.terms.start_create,
        reply_markup=keyboard
    )
    await state.set_state(router_state)


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


@router.message(
    StateFilter(router_state),
    F.photo[-1].as_('largest_photo')
)
async def done(
    message: Message, state: FSMContext, lang: str,
    largest_photo: PhotoSize
):
    state_handler = f'{router_state.state}:done'
    logger.info(state_handler)

    data = await state.get_data()

    new_instructor_dict = data['new_instructor']
    new_instructor_dict['photo_unique_id'] = largest_photo.file_unique_id
    new_instructor_dict['photo_id'] = largest_photo.file_id
    await state.update_data(
        new_instructor=new_instructor_dict
    )

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    await end_create(message=message, state=state, lang=lang)


@router.callback_query(
    StateFilter(router_state),
    F.data.in_(states_group.photo_callbacks)
)
async def cancel(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:cancel'
    logger.info(state_handler)

    data = await state.get_data()

    new_instructor_dict = data['new_instructor']
    new_instructor_dict['photo_unique_id'] = ''
    new_instructor_dict['photo_id'] = ''
    await state.update_data(
        new_instructor=new_instructor_dict
    )

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    await end_create(message=callback.message, state=state, lang=lang)


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

    buttons = terminology_lang.buttons.__dict__
    core_buttons = await core_term_lang.buttons.get_dict_with(
        *states_group.core_buttons)
    buttons.update(core_buttons)

    keyboard = await create_simply_inline_kb(
        buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.error,
        reply_markup=keyboard
    )
